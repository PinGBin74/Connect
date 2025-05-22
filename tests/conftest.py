import asyncio
import os
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncpg

from app.infrastructure.database.models import Base
from app.settings import Settings

os.environ["DB_NAME"] = "connect_test_db"
os.environ["DB_HOST"] = "0.0.0.0"
os.environ["DB_PORT"] = "5432"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "password"
os.environ["DB_DRIVER"] = "postgresql+asyncpg"

pytest_plugins = [
    "tests.fixtures.auth.auth_service",
    "tests.fixtures.users.user_repository",
    "tests.fixtures.infrastructure",
    "tests.fixtures.users.user_model",
]


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def create_test_db():
    # Connect to postgres database to create/drop test database
    sys_conn = await asyncpg.connect(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database="postgres",
    )

    # Drop test database if exists
    await sys_conn.execute(f"DROP DATABASE IF EXISTS {os.environ['DB_NAME']}")
    # Create test database
    await sys_conn.execute(f"CREATE DATABASE {os.environ['DB_NAME']}")
    await sys_conn.close()

    yield

    # Cleanup after tests
    sys_conn = await asyncpg.connect(
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=os.environ["DB_PORT"],
        database="postgres",
    )
    await sys_conn.execute(f"DROP DATABASE IF EXISTS {os.environ['DB_NAME']}")
    await sys_conn.close()


@pytest_asyncio.fixture(scope="session")
async def init_models(create_test_db):
    engine = create_async_engine(Settings().db_url, future=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(init_models) -> AsyncSession:
    engine = create_async_engine(Settings().db_url, future=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
        await engine.dispose()
