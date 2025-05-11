import httpx
from fastapi import Depends, security, Security, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.database import get_db_session
from app.infrastructure.cache import get_redis_connection
from app.exception import TokenExpired, TokenNotCorrect
from app.posts.repository.cache_post import PostCache
from app.posts.repository.post import PostRepository
from app.posts.service import PostService
from app.users.user_profile.repository import UserRepository
from app.users.user_profile.service import UserService
from app.users.auth.service import AuthService
from app.settings import Settings


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
