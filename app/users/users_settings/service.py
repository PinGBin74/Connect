from dataclasses import dataclass

from app.users.users_settings.repository import SettingsRepository


@dataclass
class UserSettingsService:
    user_settings: SettingsRepository

    async def update_settings(
        self, user_id: int, delete_photo_after_days: bool
    ) -> bool:
        return await self.user_settings.update_settings(
            user_id=user_id, delete_photo_after_days=delete_photo_after_days
        )
