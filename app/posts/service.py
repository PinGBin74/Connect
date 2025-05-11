from dataclasses import dataclass

from fastapi import HTTPException

from app.exception import PostNotFound
from app.posts.repository.cache_post import PostCache
from app.posts.repository.post import PostRepository
from app.posts.schema import PostCreateSchema, PostSchema


@dataclass
class PostService:
    post_repository: PostRepository
    post_cache: PostCache

    async def get_posts(self) -> list[PostSchema]:
        if cache_post := await self.post_cache.get_posts():
            return cache_post
        posts = await self.post_repository.get_posts()
        if posts:  # Проверяем, что список не пустой
            await self.post_cache.set_posts(posts)
        return posts
    async def create_post(self, body: PostCreateSchema, user_id: int) -> PostSchema:
        post = await self.post_repository.create_post(body, user_id)
        if not post:
            raise HTTPException(status_code=500, detail="Failed to create post")
        return PostSchema.model_validate(post)
    
    async def update_post_name(self, post_id: int, content: str, user_id: int) -> PostSchema:
        post = await self.post_repository.get_user_post(user_id=user_id, post_id=post_id)
        if not post:
            raise PostNotFound
        updated_post = await self.post_repository.update_post_name(post_id=post_id, content=content)
        if not updated_post:
            raise PostNotFound
        return PostSchema.model_validate(updated_post)
    async def delete_post(self, post_id: int, user_id: int) -> None:
        post = await self.post_repository.get_user_post(
            user_id=user_id, post_id=post_id
        )
        if not post:
            raise PostNotFound
        await self.post_repository.delete_post(post_id=post_id, user_id=user_id)
