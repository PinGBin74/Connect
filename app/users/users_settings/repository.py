from dataclasses import dataclass
from sqlalchemy import update, select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.users_settings.models import UserSettings
from app.users.user_profile.models import UserProfile


@dataclass
class SettingsRepository:
    db_session: AsyncSession

    async def update_settings(
        self, user_id: int, delete_photo_after_days: bool
    ) -> bool:
        user_query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            user_result = await session.execute(user_query)
            user = user_result.scalar_one_or_none()

            if user is None:
                return False

            settings_query = select(UserSettings).where(UserSettings.user_id == user_id)
            result = await session.execute(settings_query)
            settings = result.scalar_one_or_none()

            if settings is None:
                insert_query = insert(UserSettings).values(
                    user_id=user_id, delete_photo_after_days=delete_photo_after_days
                )
                await session.execute(insert_query)
            else:
                update_query = (
                    update(UserSettings)
                    .where(UserSettings.user_id == user_id)
                    .values(delete_photo_after_days=delete_photo_after_days)
                )
                await session.execute(update_query)

            await session.commit()
            return True
