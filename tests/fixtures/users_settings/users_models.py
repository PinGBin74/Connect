import factory.fuzzy
from pytest_factoryboy import register
from faker import Factory as FakerFactory

from app.users.users_settings.models import UserSettings


faker = FakerFactory.create()


@register(_name="UsersSettings")
class UserSettingsFactory(factory.Factory):
    class Meta:
        model = UserSettings

    user_id = factory.LazyFunction(lambda: faker.random_int())
    delete_photo_after_days = factory.LazyFunction(lambda: faker.boolean())
