from dataclasses import dataclass
import pytest

from app.posts.schema import PostCreateSchema
from tests.fixtures.posts.post_model import PostFactory


@dataclass
class FakePostRepository:

    async def create_post(self, user_data: PostCreateSchema):
        return PostFactory()


@pytest.fixture
def fake_user_repository():
    return FakePostRepository()
