from dataclasses import dataclass

from app.exception import PostNotFound
from app.posts.repository.post import PostRepository
from app.posts.schema import PostCreateSchema, PostSchema


@dataclass
class PostService:
    post_repository: PostRepository
    post_cache: PostCreateSchema

    async def get_posts(self) -> list[PostSchema]:
        if cache_post := await self.post_cache.get_tasks():
            return cache_post
        else:
            posts = await self.post_repository.get_tasks()
            posts_schema = [PostSchema.model_validate(post) for post in posts]
            await self.post_cache.set_tasks(posts_schema)
            return posts_schema

    async def create_post(self, body: PostCreateSchema, user_id: int) -> PostSchema:
        post_id = await self.post_repository.create_post(body, user_id)
        post = await self.post_repository.get_post(post_id)
        return PostSchema.model_validate(post)

    async def update_post_name(
        self, post_id: int, username: str, user_id: int
    ) -> PostSchema:
        post = await self.post_repository.get_user_post(
            user_id=user_id, post_id=post_id
        )
        if not post:
            raise PostNotFound
        post = await self.post_repository.update_post_name(
            post_id=post_id, username=username
        )
        return PostSchema.model_validate(post)

    async def delete_post(self, post_id: int, user_id: int) -> None:
        post = await self.post_repository.get_user_task(
            user_id=user_id, post_id=post_id
        )
        if not post:
            raise PostNotFound
        await self.post_repository.delete_task(post_id=post_id, user_id=user_id)
