from dataclasses import dataclass
import pytest

from app.users.user_profile.schema import UserCreateSchema
from tests.fixtures.users.user_model import UserFactory


@dataclass
class FakeUserRepository:

    async def create_user(self, user_data: UserCreateSchema):
        return UserFactory()


@pytest.fixture
def fake_user_repository():
    return FakeUserRepository()
