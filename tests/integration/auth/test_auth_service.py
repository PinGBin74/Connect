import pytest
import pytest_asyncio
from sqlalchemy import select, insert

from app.users.user_profile.models import UserProfile
from app.users.auth.service import AuthService
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.service import UserService
from app.settings import Settings
from app.exception import UserAlreadyExists

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def user_repository(db_session):
    return UserRepository(db_session)


@pytest_asyncio.fixture
async def auth_service(user_repository):
    return AuthService(user_repository=user_repository, settings=Settings())


@pytest_asyncio.fixture
async def user_service(user_repository, auth_service):
    return UserService(user_repository=user_repository, auth_service=auth_service)


async def test_base_login__success(auth_service, db_session):
    username = "test_username"
    password = "test_password"

    query = insert(UserProfile).values(username=username, password=password)
    await db_session.execute(query)
    await db_session.commit()
    await db_session.flush()
    login_user = (
        await db_session.execute(
            select(UserProfile).where(UserProfile.username == username)
        )
    ).scalar_one_or_none()

    user_data = await auth_service.login(username=username, password=password)

    assert login_user is not None
    assert user_data.user_id == login_user.id


async def test_base_create_user__success(user_service, db_session):
    username = "test_username1"
    password = "test_username"

    user_data = await user_service.create_user(username=username, password=password)
    assert user_data is not None
    assert user_data.user_id is not None


async def test_base_create_user__failure(user_service, db_session):
    username = "test_username2"
    password = "test_username"

    await user_service.create_user(username=username, password=password)

    with pytest.raises(UserAlreadyExists) as e:
        await user_service.create_user(username=username, password=password)

    assert str(e.value) == "User already exists"
