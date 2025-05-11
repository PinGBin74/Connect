from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.posts.models import Posts
from app.posts.schema import PostSchema


class PostRepository:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_posts(self) -> list[PostSchema]:
        posts = await self.db_session.execute(select(Posts))
        posts = posts.scalars().all()
        return [PostSchema.model_validate(post) for post in posts]

    async def get_post(self, post_id: int) -> Posts | None:
        result = await self.db_session.execute(select(Posts).where(Posts.id == post_id))
        return result.scalar_one_or_none()

    async def get_user_post(self, post_id: int, user_id: int) -> Posts | None:
        query = select(Posts).where(Posts.id == post_id, Posts.user_id == user_id)
        async with self.db_session as session:
            post: Posts = (await session.execute(query)).scalar_one_or_none()
        return post

    async def create_post(self, post_data: dict) -> Posts:
        post = Posts(**post_data)
        self.db_session.add(post)
        await self.db_session.commit()
        await self.db_session.refresh(post)
        return post

    async def delete_post(self, post_id: int, user_id: int) -> None:
        query = delete(Posts).where(Posts.id == post_id, Posts.user_id == user_id)
        async with self.db_session as session:
            await session.execute(query)
            await session.commit()

    async def update_post_name(self, post_id: int, username: str) -> Posts:
        query = (
            update(Posts)
            .where(Posts.id == post_id)
            .values(username=username)
            .returning(Posts.id)
        )
        async with self.db_session as session:
            post_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            await session.flush()
            return await self.get_post(post_id)
