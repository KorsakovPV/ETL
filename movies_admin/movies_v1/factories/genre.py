import datetime

from factory import Faker, fuzzy
from factory.django import DjangoModelFactory
from pytz import UTC

from movies_v1.models import Genre, FilmWorkGenre


class GenreFactory(DjangoModelFactory):
    id = Faker('uuid4')
    name = Faker('company')
    description = Faker('sentence', nb_words=128, variable_nb_words=True)
    created = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(2020, 1, 1, tzinfo=UTC))
    modified = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(2020, 1, 1, tzinfo=UTC))

    class Meta:
        model = Genre


class FilmWorkGenreFactory(DjangoModelFactory):
    id = Faker('uuid4')
    created = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(2020, 1, 1, tzinfo=UTC))
    modified = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(2020, 1, 1, tzinfo=UTC))

    class Meta:
        model = FilmWorkGenre
