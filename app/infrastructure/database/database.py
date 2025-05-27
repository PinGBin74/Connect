from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
import os

from app.settings import Settings


connect_args = {}
if os.getenv("ENVIRONMENT") == "production":
    connect_args["ssl"] = "require"

engine = create_async_engine(
    url=Settings().db_url,
    future=True,
    echo=True,
    pool_pre_ping=True,
    connect_args=connect_args,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session
