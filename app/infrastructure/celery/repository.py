import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select, and_
from app.posts.models import Posts
import redis
import datetime as dt

from app.users.users_settings.models import UserSettings


class PostRepository:
    def __init__(self, db_session: AsyncSession, redis_client: redis.Redis):
        self.redis = redis_client
        self.db_session = db_session

    async def _check_user_delete_settings(self, user_id: int) -> bool:
        """
        Check if user has delete_photo_after_days=True in settings
        :param user_id: User ID to check
        :return: True if user has delete_photo_after_days=True, False otherwise
        """
        settings_query = select(UserSettings).where(
            and_(
                UserSettings.user_id == user_id,
                UserSettings.delete_photo_after_days.is_(True),
            )
        )
        settings = await self.db_session.execute(settings_query)
        return settings.scalar_one_or_none() is not None

    async def delete_old_posts(self, hours: int = 168) -> int:
        """
        Delete posts older than the specified number of hours for users who have delete_photo_after_days=True
        :param hours: Quantity of hours
        :return: Quantity of deleted posts
        """
        try:
            old_posts_query = select(Posts).where(
                Posts.created_at < dt.datetime.utcnow() - dt.timedelta(hours=hours)
            )
            old_posts = await self.db_session.execute(old_posts_query)
            old_posts = old_posts.scalars().all()

            deleted_count = 0
            for post in old_posts:
                if await self._check_user_delete_settings(post.user_id):
                    delete_query = delete(Posts).where(Posts.id == post.id)
                    await self.db_session.execute(delete_query)
                    deleted_count += 1

            await self.db_session.commit()
            return deleted_count
        except Exception:
            await self.db_session.rollback()
            return 0

    async def delete_old_posts_from_redis(self, days: int = 30) -> int:
        """
        Delete posts older than the specified number of days for users who have delete_photo_after_days=True
        :param days: Quantity of days
        :return: Quantity of deleted posts
        """
        try:
            cutoff_timestamp = (
                dt.datetime.utcnow() - dt.timedelta(days=days)
            ).timestamp()
            deleted_count = 0

            post_keys = self.redis.keys("posts:*")
            if not post_keys:
                return 0

            for key in post_keys:
                try:
                    post_data = self.redis.hgetall(key)
                    if not post_data:
                        continue

                    created_at = dt.datetime.strptime(
                        post_data["created_at"], "%Y-%m-%d %H:%M:%S"
                    )
                    if created_at.timestamp() < cutoff_timestamp:
                        # Check user settings before deleting
                        user_id = int(post_data.get("user_id", 0))
                        if user_id and await self._check_user_delete_settings(user_id):
                            self.redis.delete(key)
                            deleted_count += 1
                except (json.JSONDecodeError, KeyError, ValueError):
                    continue

            return deleted_count
        except Exception:
            return 0
