import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.posts.models import Posts
import redis
import datetime as dt


class PostRepository:
    def __init__(self, db_session: AsyncSession, redis_client: redis.Redis):
        self.redis = redis_client
        self.db_session = db_session

    async def delete_old_posts(self, hours: int = 168) -> int:
        """
        Delete posts older than the specified number of hours
        :param hours: Quantity of hours
        :return: Quantity of deleted posts
        """
        try:
            query = delete(Posts).where(
                Posts.created_at < dt.datetime.utcnow() - dt.timedelta(hours=hours)
            )
            result = await self.db_session.execute(query)
            await self.db_session.commit()
            return result.rowcount
        except Exception:
            await self.db_session.rollback()
            return 0

    async def delete_old_posts_from_redis(self, days: int = 30) -> int:
        """
        Delete posts older than the specified number of days
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
                        self.redis.delete(key)
                        deleted_count += 1
                except (json.JSONDecodeError, KeyError):
                    continue

            return deleted_count
        except Exception:
            return 0
