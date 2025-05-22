import pytest
import pytest_asyncio
from sqlalchemy import insert, select
from redis.asyncio import Redis

from app.posts.models import Posts
from app.posts.repository.cache_post import PostCache
from app.posts.repository.post import PostRepository
from app.posts.service import PostService
from app.posts.schema import PostCreateSchema
from app.users.user_profile.models import UserProfile
from app.exception import PostNotFound

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def post_repository(db_session):
    return PostRepository(db_session)


@pytest_asyncio.fixture
async def redis_client():
    return Redis(host="localhost", port=6379, db=0, decode_responses=True)


@pytest_asyncio.fixture
async def post_cache(redis_client):
    return PostCache(redis=redis_client)


@pytest_asyncio.fixture
async def post_service(post_repository, post_cache):
    return PostService(post_repository=post_repository, post_cache=post_cache)


async def test_create_post__success(post_service, db_session):
    # First create a user
    user_query = insert(UserProfile).values(
        username="test_username_1", password="test_password", photo_url=None
    )
    await db_session.execute(user_query)
    await db_session.commit()
    await db_session.flush()

    # Get the created user's ID
    result = await db_session.execute(
        select(UserProfile).where(UserProfile.username == "test_username_1")
    )
    user = result.scalar_one()
    user_id = user.id

    content = "test"
    photo_url = "test"

    post = await post_service.create_post(
        body=PostCreateSchema(content=content, photo_url=photo_url), user_id=user_id
    )

    assert post is not None
    assert post.content == content
    assert post.photo_url == photo_url
    assert post.user_id == user_id
    assert post.username == "test_username_1"


async def test_get_post__success(post_service, db_session):
    unique_username = "test_username_2"
    user_query = insert(UserProfile).values(
        username=unique_username, password="test_password", photo_url=None
    )
    await db_session.execute(user_query)
    await db_session.commit()
    await db_session.flush()

    # Get the created user's ID
    result = await db_session.execute(
        select(UserProfile).where(UserProfile.username == unique_username)
    )
    user = result.scalar_one()
    user_id = user.id

    content = "test_content_2"
    photo_url = "test"

    # Create a post
    post_query = insert(Posts).values(
        content=content, photo_url=photo_url, user_id=user_id, username=unique_username
    )
    await db_session.execute(post_query)
    await db_session.commit()
    await db_session.flush()

    # Get the created post's ID
    result = await db_session.execute(select(Posts).where(Posts.content == content))
    created_post = result.scalar_one()
    post_id = created_post.id

    post = await post_service.get_post(post_id)

    assert post is not None
    assert post.id == post_id
    assert post.content == content
    assert post.photo_url == photo_url
    assert post.user_id == user_id
    assert post.username == unique_username


async def test_get_post__not_found(post_service, db_session):
    post_id = 10011
    post = await post_service.get_post(post_id)

    assert post is None


async def test_get_posts__success(post_service, db_session):
    posts = await post_service.get_posts()
    assert posts is not None
    assert len(posts) > 0 or posts == []


async def test_delete_post__success(post_service, db_session):
    # First create a user
    unique_username = "test_username_delete"
    user_query = insert(UserProfile).values(
        username=unique_username, password="test_password", photo_url=None
    )
    await db_session.execute(user_query)
    await db_session.commit()
    await db_session.flush()

    # Get the created user's ID
    result = await db_session.execute(
        select(UserProfile).where(UserProfile.username == unique_username)
    )
    user = result.scalar_one()
    user_id = user.id

    content = "test_content_delete"
    photo_url = "test"

    # Create a post
    post_query = insert(Posts).values(
        content=content, photo_url=photo_url, user_id=user_id, username=unique_username
    )
    await db_session.execute(post_query)
    await db_session.commit()
    await db_session.flush()

    # Get the created post's ID
    result = await db_session.execute(select(Posts).where(Posts.content == content))
    created_post = result.scalar_one()
    post_id = created_post.id

    # Delete the post
    await post_service.delete_post(post_id, user_id)

    # Verify the post is deleted
    result = await db_session.execute(select(Posts).where(Posts.id == post_id))
    deleted_post = result.scalar_one_or_none()
    assert deleted_post is None


async def test_patch_post_success(post_service, db_session):
    # First create a user
    unique_username = "test_username_patch"
    user_query = insert(UserProfile).values(
        username=unique_username, password="test_password", photo_url=None
    )
    await db_session.execute(user_query)
    await db_session.commit()
    await db_session.flush()

    # Get the created user's ID

    result = await db_session.execute(
        select(UserProfile).where(UserProfile.username == unique_username)
    )
    user = result.scalar_one()
    user_id = user.id

    content = "test_content_delete"
    photo_url = "test"

    # Create a post
    post_query = insert(Posts).values(
        content=content, photo_url=photo_url, user_id=user_id, username=unique_username
    )
    await db_session.execute(post_query)
    await db_session.commit()
    await db_session.flush()

    # Get the created post's ID
    result = await db_session.execute(select(Posts).where(Posts.content == content))
    created_post = result.scalar_one()
    post_id = created_post.id

    new_content = "new_content"

    updated_post = await post_service.update_post_name(
        post_id=post_id, content=new_content, user_id=user_id
    )
    assert updated_post is not None
    assert updated_post.content == new_content
    assert updated_post.id == post_id
    assert updated_post.user_id == user_id


async def test_patch_post__not_found(post_service, db_session):
    post_id = 10011
    new_content = "new_content"
    with pytest.raises(PostNotFound):
        await post_service.update_post_name(
            post_id=post_id, content=new_content, user_id=1
        )
