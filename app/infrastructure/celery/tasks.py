from app.infrastructure.celery.conf import celery
from app.infrastructure.celery.service import PostService
import asyncio


def run_async(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()
        asyncio.set_event_loop(None)


@celery.task(name="app.infrastructure.celery.tasks.delete_old_posts")
def delete_old_posts(hours: int = 168) -> int:
    """
    Celery задача для удаления старых постов
    :param hours: Количество часов
    :return: Количество удаленных постов
    """
    return run_async(PostService.delete_old_posts(hours))


@celery.task(name="app.infrastructure.celery.tasks.delete_old_posts_from_redis")
def delete_old_posts_from_redis(days: int = 30) -> int:
    """
    Celery задача для удаления старых постов из Redis
    :param days: Количество дней
    :return: Количество удаленных постов
    """
    return run_async(PostService.delete_old_posts_from_redis(days))


# @celery.task(name='app.infrastructure.celery.tasks.periodic_delete_posts')
# def periodic_delete_posts() -> None:
#     """
#     Периодическая задача для удаления старых постов
#     - Удаляет посты из PostgreSQL старше 7 дней
#     - Удаляет посты из Redis старше 30 дней
#     """
#     run_async(PostService.delete_old_posts(days=7))
#     run_async(PostService.delete_old_posts_from_redis(days=30))
