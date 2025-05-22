import datetime
import factory.fuzzy
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.posts.models import Posts


faker = FakerFactory.create()


@register(_name="post")
class PostFactory(factory.Factory):
    class Meta:
        model = Posts

    id = factory.LazyFunction(lambda: faker.random_int())
    username = factory.LazyFunction(lambda: faker.user_name())
    created_at = factory.LazyFunction(lambda: datetime.utcnow())
    content = factory.LazyFunction(lambda: faker.text())
    user_id = factory.LazyFunction(lambda: faker.randrom_int())
    photo_url = factory.LazyFunction(lambda: faker.image_url())
