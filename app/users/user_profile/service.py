from dataclasses import dataclass

from app.exception import UserAlreadyExists
from app.users.auth.schema import UserLoginSchema
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.schema import UserCreateSchema


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, username: str, password: str) -> UserLoginSchema:
        # Check if user already exists
        existing_user = await self.user_repository.get_user_by_username(username)
        if existing_user:
            raise UserAlreadyExists(UserAlreadyExists.detail)

        user_data = UserCreateSchema(username=username, password=password)
        user = await self.user_repository.create_user(user_data)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)

    async def create_user_with_photo(
        self, user_data: UserCreateSchema
    ) -> UserLoginSchema:
        # Check if user already exists
        existing_user = await self.user_repository.get_user_by_username(
            user_data.username
        )
        if existing_user:
            raise UserAlreadyExists(UserAlreadyExists.detail)

        user = await self.user_repository.create_user(user_data)
        access_token = self.auth_service.generate_access_token(user_id=user.id)
        return UserLoginSchema(user_id=user.id, access_token=access_token)
