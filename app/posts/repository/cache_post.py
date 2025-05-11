from redis import asyncio as Redis
import json

from app.posts.schema import PostSchema


class PostCache:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_posts(self) -> list[PostSchema]:
        async with self.redis as redis:
            posts_json = await redis.lrange("posts", 0, -1)
            return [PostSchema.model_validate(json.load(post)) for post in posts_json]

    async def set_posts(self, posts: list[PostSchema]):
        posts_json = [post.model_dump_json() for post in posts]
        async with self.redis as redis:
            await redis.delete("posts")
            if posts_json:
                await redis.rpush("posts", *posts_json)
