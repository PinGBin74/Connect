import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from app.infrastructure.database.models import Base
from app.settings import Settings

from app.users.user_profile.models import UserProfile
from app.posts.models import Posts
from app.users.subscription.models import subscriptions

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        include_schemas=True,
        version_table_schema=target_metadata.schema,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode with async engine"""
    connectable = create_async_engine(Settings().db_url, future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


# Запуск миграций
asyncio.run(run_migrations_online())
