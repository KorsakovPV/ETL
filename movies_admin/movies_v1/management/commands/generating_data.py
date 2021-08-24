import logging
import random
from tqdm import tqdm

import pyprind
from django.core.management.base import BaseCommand

from movies_v1.factories.film_work import FilmWorkFactory
from movies_v1.factories.genre import GenreFactory, FilmWorkGenreFactory
from movies_v1.factories.person import PersonFactory, FilmWorkPersonFactory
from movies_v1.factories.user import UserFactory
from movies_v1.models import User, Genre, FilmWork, Person, FilmWorkGenre, FilmWorkPerson


class Command(BaseCommand):
    help = 'Generating data.'

    USER = 10
    GENRE = 100
    PERSON = 1000
    FILMWORK_FILM = 101
    FILMWORK_SERIES = 202
    FILMWORK_MIN_GENRE = 0
    FILMWORK_MAX_GENRE = 5
    FILMWORK_MIN_PERSONS = 0
    FILMWORK_MAX_PERSONS = 5
    FILMWORK_GENRES_PERSONS = 72000
    PADGE = 10000

    def handle(self, *args, **options):
        """
        python manage.py generating_data
        """

        logging.basicConfig(filename="sample.log", level=logging.INFO)

        User.objects.exclude(is_superuser=True).delete()
        Genre.objects.all().delete()
        Person.objects.all().delete()
        FilmWork.objects.all().delete()

        self.generating_users()

        self.generating_genres()
        self.all_genre = Genre.objects.all()

        self.generating_persons()
        self.all_person = Person.objects.all()

        self.generating_film(type='series', counter=self.FILMWORK_SERIES)

        self.generating_film(type='film', counter=self.FILMWORK_FILM)

    def generating_film(self, type, counter):
        film_count = counter - FilmWork.objects.filter(type=type).count()
        if film_count > 0:
            films = []
            genres = []
            persons = []
            # bar = pyprind.ProgBar(film_count, title=f'Generating FilmWork {type}.')
            pbar = tqdm(total=film_count)
            for _ in range(film_count):
                # bar.update()
                pbar.update(1)
                film = FilmWorkFactory.build(type=type)

                film_genres = {random.choice(self.all_genre) for _ in
                               range(random.randint(self.FILMWORK_MIN_GENRE, self.FILMWORK_MAX_GENRE))}
                for film_genre in film_genres:
                    genres.append(FilmWorkGenreFactory.build(film_work=film, genre=film_genre))

                film_persons = {random.choice(self.all_person) for _ in
                                range(random.randint(self.FILMWORK_MIN_PERSONS, self.FILMWORK_MAX_PERSONS))}
                for film_person in film_persons:
                    persons.append(FilmWorkPersonFactory.build(film_work=film, person=film_person))

                films.append(film)
                if len(films) > self.PADGE:
                    FilmWork.objects.bulk_create(films)
                    films = []
                    FilmWorkGenre.objects.bulk_create(genres)
                    genres = []
                    FilmWorkPerson.objects.bulk_create(persons)
                    persons = []
            FilmWork.objects.bulk_create(films)
            FilmWorkGenre.objects.bulk_create(genres)
            FilmWorkPerson.objects.bulk_create(persons)

    def generating_persons(self):
        person_count = self.PERSON - Person.objects.all().count()
        if person_count > 0:
            persons = PersonFactory.build_batch(person_count)
            Person.objects.bulk_create(persons)

    def generating_genres(self):
        genre_count = self.GENRE - Genre.objects.all().count()
        if genre_count > 0:
            genres = GenreFactory.build_batch(genre_count)
            Genre.objects.bulk_create(genres)

    def generating_users(self):
        user_count = self.USER - User.objects.all().count()
        if user_count > 0:
            user = UserFactory.build_batch(user_count)
            User.objects.bulk_create(user)
