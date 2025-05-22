import pytest
from unittest.mock import AsyncMock

from app.users.users_settings.service import UserSettingsService


pytestmark = pytest.mark.asyncio


async def test_update_settings__success():
    # Arrange
    mock_repository = AsyncMock()
    service = UserSettingsService(user_settings=mock_repository)
    mock_repository.update_settings.return_value = True

    user_id = 1
    delete_photo_after_days = True

    # Act
    result = await service.update_settings(
        user_id=user_id, delete_photo_after_days=delete_photo_after_days
    )

    # Assert
    assert result is True
    mock_repository.update_settings.assert_called_once_with(
        user_id=user_id, delete_photo_after_days=delete_photo_after_days
    )
