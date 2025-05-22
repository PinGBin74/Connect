import pytest_asyncio

from app.settings import Settings
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository


@pytest_asyncio.fixture
async def mock_auth_service(fake_user_repository):
    return AuthService(
        user_repository=fake_user_repository,
        settings=Settings(),
    )


@pytest_asyncio.fixture
async def auth_service(get_db_session):
    return AuthService(
        user_repository=UserRepository(db_session=get_db_session),
        settings=Settings(),
    )
