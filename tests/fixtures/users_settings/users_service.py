import pytest_asyncio

from app.settings import Settings
from app.users.users_settings.repository import SettingsRepository
from app.users.users_settings.service import UserSettingsService


@pytest_asyncio.fixture
async def mock_auth_service(fake_user_repository):
    return UserSettingsService(
        settings_repository=fake_user_repository,
        settings=Settings(),
    )


@pytest_asyncio.fixture
async def auth_service(get_db_session):
    return UserSettingsService(
        settings_repository=SettingsRepository(db_session=get_db_session),
        settings=Settings(),
    )
