from app.infrastructure.database.database import AsyncSessionFactory
from app.infrastructure.celery.repository import PostRepository
import redis


class PostService:
    @staticmethod
    async def delete_old_posts(hours: int = 1) -> int:
        """
        Delete old posts through celery
        :param hours: Quantity of hours
        :return: Quantity of deleted posts
        """
        async with AsyncSessionFactory() as session:
            redis_client = redis.Redis(
                host="localhost", port=6379, db=0, decode_responses=True
            )
            try:
                repository = PostRepository(session, redis_client)
                return await repository.delete_old_posts(hours)
            finally:
                redis_client.close()

    @staticmethod
    async def delete_old_posts_from_redis(days: int = 7) -> int:
        """
        Delete old posts through celery
        :param days: Quantity of days
        :return: Quantity of deleted posts
        """
        async with AsyncSessionFactory() as session:
            redis_client = redis.Redis(
                host="localhost", port=6379, db=0, decode_responses=True
            )
            try:
                repository = PostRepository(session, redis_client)
                return await repository.delete_old_posts_from_redis(days)
            finally:
                redis_client.close()
