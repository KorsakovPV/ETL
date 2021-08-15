import datetime

from factory import Faker, fuzzy
from factory.django import DjangoModelFactory
from pytz import UTC

from movies_v1.models import FilmWork, MPAARatingType, FilmWorkType


class FilmWorkFactory(DjangoModelFactory):
    id = Faker('uuid4')
    title = Faker('company')
    description = Faker('sentence', nb_words=128, variable_nb_words=True)
    creation_date = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(2000, 1, 1, tzinfo=UTC))
    certificate = Faker('company')
    mpaa_rating = fuzzy.FuzzyChoice(MPAARatingType)
    rating = fuzzy.FuzzyDecimal(0, 9.9)
    type = fuzzy.FuzzyChoice(FilmWorkType)
    created = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))
    modified = fuzzy.FuzzyDateTime(start_dt=datetime.datetime(1940, 1, 1, tzinfo=UTC))

    class Meta:
        model = FilmWork
