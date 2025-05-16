from app.infrastructure.celery.conf import celery
from app.infrastructure.celery.service import PostService
import asyncio


@celery.task(name="app.infrastructure.celery.tasks.delete_old_posts")
def delete_old_posts(hours: int = 1) -> int:
    """
    Celery task for deleting old posts
    :param hours: Quantity of hours
    :return: Quantity of deleted posts
    """
    return asyncio.run(PostService.delete_old_posts(hours))
