from celery import Celery
from celery.schedules import crontab
from app.settings import Settings

settings = Settings()

celery = Celery(
    "app.infrastructure.celery",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.infrastructure.celery.tasks"],
)
celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        "delete-old-posts": {
            "task": "app.infrastructure.celery.tasks.delete_old_posts",
            "schedule": crontab(hour="*/6"),  # Run every 6 hours
        },
        "delete-old-posts-from-redis": {
            "task": "app.infrastructure.celery.tasks.delete_old_posts_from_redis",
            "schedule": crontab(hour="*/12"),  # Run every 12 hours
        },
        # 'periodic-delete-posts': {
        #     'task': 'app.infrastructure.celery.tasks.periodic_delete_posts',
        #     'schedule': crontab(hour=0, minute=0, day_of_week='monday'),  # Запуск каждый понедельник в полночь
        # },
    },
)
