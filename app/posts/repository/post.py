from datetime import datetime as dt
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.posts.models import Posts
from app.posts.schema import PostCreateSchema, PostSchema
from app.users.user_profile.models import UserProfile


class PostRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_posts(self) -> list[PostSchema]:
        posts = await self.db_session.execute(select(Posts))
        posts = posts.scalars().all()
        valid_posts = [
            PostSchema.model_validate(post) for post in posts if post is not None
        ]
        return valid_posts

    async def get_post(self, post_id: int) -> Posts | None:
        result = await self.db_session.execute(select(Posts).where(Posts.id == post_id))
        return result.scalar_one_or_none()

    async def get_user_posts_by_username(
        self, post_id: int, user_id: int
    ) -> Posts | None:
        query = select(Posts).where(Posts.id == post_id, Posts.user_id == user_id)
        async with self.db_session as session:
            post: Posts = (await session.execute(query)).scalar_one_or_none()
        return post

    async def create_post(self, post_data: PostCreateSchema, user_id: int) -> Posts:
        stmt = select(UserProfile.username).where(UserProfile.id == user_id)
        username = (await self.db_session.execute(stmt)).scalar_one_or_none()
        post = Posts(
            content=post_data.content,
            photo_url=post_data.photo_url,
            user_id=user_id,
            username=username,
            created_at=dt.utcnow(),
        )
        self.db_session.add(post)
        await self.db_session.commit()
        await self.db_session.refresh(post)
        return post

    async def update_post_name(self, post_id: int, content: str) -> Posts | None:
        query = (
            update(Posts)
            .where(Posts.id == post_id)
            .values(content=content)
            .returning(Posts)
        )
        result = await self.db_session.execute(query)
        post = result.scalar_one_or_none()
        if post is None:
            return None
        await self.db_session.commit()
        return post

    async def delete_post(self, post_id: int, user_id: int) -> None:
        query = delete(Posts).where(Posts.id == post_id, Posts.user_id == user_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def get_posts_by_username(self, username: str) -> list[PostSchema]:
        query = select(Posts).where(Posts.username == username)
        result = await self.db_session.execute(query)
        posts = result.scalars().all()
        return [PostSchema.model_validate(post) for post in posts if post is not None]
