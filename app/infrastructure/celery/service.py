from app.infrastructure.database.database import AsyncSessionFactory
from app.infrastructure.celery.repository import PostRepository


class PostService:
    @staticmethod
    async def delete_old_posts(hours: int = 1) -> int:
        """
        Delete old posts through service
        :param hours: Quantity of hours
        :return: Quantity of deleted posts
        """
        async with AsyncSessionFactory() as session:
            repository = PostRepository(session)
            return await repository.delete_old_posts(hours)
