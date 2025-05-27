from redis import asyncio as redis

from app.settings import Settings


def get_redis_connection() -> redis.Redis:
    settings = Settings()
    return redis.from_url(settings.redis_url, decode_responses=True)
