import datetime

from factory import Faker, fuzzy
from factory.django import DjangoModelFactory
from pytz import UTC

from movies_v1.models import Person, FilmWorkPerson, RoleType


class PersonFactory(DjangoModelFactory):
    id = Faker('uuid4')
    full_name = Faker('name')
    birth_date = Faker('date')
    created = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))
    modified = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))

    class Meta:
        model = Person


class FilmWorkPersonFactory(DjangoModelFactory):
    id = Faker('uuid4')
    role = fuzzy.FuzzyChoice(RoleType)
    created = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))
    modified = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))

    class Meta:
        model = FilmWorkPerson
