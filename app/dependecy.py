import httpx
from fastapi import Depends, security, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db_session
from app.infrastructure.cache import get_redis_connection
from app.exception import TokenExpired, TokenNotCorrect
from app.posts.repository.cache_post import PostCache
from app.posts.repository.post import PostRepository
from app.posts.service import PostService
from app.users.subscription.repository import SubscriptionRepository
from app.users.subscription.service import SubscripionService
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.service import UserService
from app.users.auth.service import AuthService
from app.settings import Settings
from app.users.users_settings.repository import SettingsRepository
from app.users.users_settings.service import UserSettingsService


def get_settings_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> SettingsRepository:
    return SettingsRepository(db_session=db_session)


def get_settings_service(
    settings_repository: SettingsRepository = Depends(get_settings_repository),
) -> UserSettingsService:
    return UserSettingsService(user_settings=settings_repository)


async def get_posts_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> PostRepository:
    return PostRepository(db_session)


async def get_posts_cache_repository() -> PostCache:
    redis_connection = get_redis_connection()
    return PostCache(redis_connection)


async def get_user_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_post_service(
    post_repository: PostRepository = Depends(get_posts_repository),
    post_cache: PostCache = Depends(get_posts_cache_repository),
) -> PostService:
    return PostService(post_repository=post_repository, post_cache=post_cache)


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
    )


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


async def get_subscription_reposiory(
    db_session: AsyncSession = Depends(get_db_session),
) -> SubscriptionRepository:
    return SubscriptionRepository(db_session=db_session)


async def get_subscription_service(
    subscription_repository: SubscriptionRepository = Depends(
        get_subscription_reposiory
    ),
) -> SubscripionService:
    return SubscripionService(subscription_repository=subscription_repository)


reusable_oauth2 = security.HTTPBearer()


async def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    """
    Verify user by access_token.
    """
    try:
        user_id = auth_service.get_user_id_from_access_token(token.credentials)

    except TokenExpired as e:
        raise HTTPException(status_code=401, detail=e.detail)
    except TokenNotCorrect as e:
        raise HTTPException(status_code=401, detail=e.detail)
    return user_id


def get_current_user_id(
    token: str = Depends(security.HTTPBearer()),
    auth_service: AuthService = Depends(lambda: AuthService(None, Settings())),
) -> int:
    try:
        return auth_service.get_user_id_from_access_token(token.credentials)
    except (TokenExpired, TokenNotCorrect):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
