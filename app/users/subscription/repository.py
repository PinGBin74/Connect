from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.models import Posts
from app.posts.schema import PostSchema
from app.users.subscription.schema import SubscriptionResponse
from app.users.user_profile.models import UserProfile
from app.users.subscription.models import subscriptions


class SubscriptionRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def subscribe(self, follower_id: int, followed_username: str) -> bool:
        async with self.db_session as session:
            query = select(UserProfile).where(UserProfile.username == followed_username)
            result = await session.execute(query)
            users = result.scalars().all()
            if not users or len(users) > 1:
                return False

            followed_id = users[0].id
            if followed_id == follower_id:
                return False

            # Проверяем, существует ли уже такая подписка
            check_query = select(subscriptions).where(
                (subscriptions.c.follower_id == follower_id)
                & (subscriptions.c.following_id == followed_id)
            )
            result = await session.execute(check_query)
            if result.first():
                return False

            query = insert(subscriptions).values(
                follower_id=follower_id, following_id=followed_id
            )
            await session.execute(query)
            await session.commit()
            return True

    async def unsubscribe(self, follower_id: int, followed_username: str) -> bool:
        async with self.db_session as session:
            query = select(UserProfile).where(UserProfile.username == followed_username)
            result = await session.execute(query)
            users = result.scalars().all()
            if not users or len(users) > 1:
                return False

            followed_id = users[0].id

            query = delete(subscriptions).where(
                (subscriptions.c.follower_id == follower_id)
                & (subscriptions.c.following_id == followed_id)
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    async def get_following(self, follower_id: int) -> list[SubscriptionResponse]:
        async with self.db_session as session:
            query = (
                select(UserProfile)
                .join(subscriptions, subscriptions.c.following_id == UserProfile.id)
                .where(subscriptions.c.follower_id == follower_id)
            )
            result = await session.execute(query)
            users = result.scalars().all()
            return [SubscriptionResponse.model_validate(user) for user in users]

    async def get_following_posts(self, follower_id: int) -> list[PostSchema]:
        async with self.db_session as session:
            query = (
                select(Posts)
                .join(subscriptions, subscriptions.c.following_id == Posts.user_id)
                .where(subscriptions.c.follower_id == follower_id)
                .order_by(Posts.created_at.desc())
            )
            result = await session.execute(query)
            posts = result.scalars().all()
            return [PostSchema.model_validate(post) for post in posts]
