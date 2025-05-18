from dataclasses import dataclass
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.user_profile.models import UserProfile
from app.users.user_profile.schema import UserCreateSchema
from app.users.users_settings.models import UserSettings


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def create_user(self, user_data: UserCreateSchema) -> UserProfile:
        async with self.db_session as session:
            user_query = (
                insert(UserProfile)
                .values(
                    username=user_data.username,
                    password=user_data.password,
                    photo_url=user_data.photo_url,
                )
                .returning(UserProfile)
            )
            result = await session.execute(user_query)
            user = result.scalar_one()
            settings_query = insert(UserSettings).values(
                user_id=user.id, delete_photo_after_days=True
            )
            await session.execute(settings_query)

            await session.commit()
            return user

    async def get_user(self, user_id) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.id == user_id)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserProfile | None:
        """
        Get user from DataBase by username.
        """
        query = select(UserProfile).where(UserProfile.username == username)
        async with self.db_session as session:
            return (await session.execute(query)).scalar_one_or_none()
