from factory import Faker, PostGenerationMethodCall
from factory.django import DjangoModelFactory

from movies_v1.models import User

DEFAULT_PASSWORD = 'test1'


class UserFactory(DjangoModelFactory):
    username = Faker('user_name')
    email = Faker('email')
    password = PostGenerationMethodCall('set_password', DEFAULT_PASSWORD)
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    class Meta:
        model = User
