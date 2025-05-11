import httpx

from app.exception import TokenExpired, TokenNotCorrect
from app.infrastructure.cache.accessor import get_redis_connection
from app.infrastructure.database.database import get_db_session
from app.users.auth.client.google_client import GoogleClient
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Depends, HTTPException, Security, security
from app.settings import Settings
from app.users.auth.client.yandex import YandexClient
from app.users.auth.repository import UserCache
from app.users.auth.service import AuthService
from app.users.user_profle.repository import UserRepository
from app.users.user_profle.service import UserService


async def get_async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient()


async def get_google_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> GoogleClient:
    return GoogleClient(settings=Settings(), async_client=async_client)


async def get_user_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session)


async def get_yandex_client(
    async_client: httpx.AsyncClient = Depends(get_async_client),
) -> YandexClient:
    return YandexClient(settings=Settings(), async_client=async_client)


async def get_user_service_cache() -> UserCache:
    redis_connection = get_redis_connection()
    return UserCache(redis_connection)


async def get_auth_service(
    user_repository: UserRepository = Depends(get_user_repository),
    google_client: GoogleClient = Depends(get_google_client),
    yandex_client: YandexClient = Depends(get_yandex_client),
    user_cache: UserCache = Depends(get_user_service_cache),
) -> AuthService:
    return AuthService(
        user_repository=user_repository,
        settings=Settings(),
        google_client=google_client,
        yandex_client=yandex_client,
        user_cache=user_cache,
    )


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
) -> UserService:
    return UserService(user_repository=user_repository, auth_service=auth_service)


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
