import factory

from src.my_apps.base_factories import BaseFactory
from src.my_apps.users.models import User


class UserFactory(BaseFactory):
    class Meta:
        model = User
        sqlalchemy_get_or_create = ('username', 'email')

    username = factory.Faker('name')
    hashed_password = factory.Faker('password')
    email = factory.Faker('email')

