import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

User = get_user_model()


class MPAARatingType(models.TextChoices):
    G = 'general', _('G — General audiences')
    PG = 'parental_guidance', _('PG — Parental guidance suggested')
    PG_13 = 'parental_guidance_strong', _('PG-13 — Parents strongly cautioned')
    R = 'restricted', _('R — Restricted')
    NC_17 = 'no_one_17_under', _('NC-17 — No One 17 & Under Admitted')


class RoleType(models.TextChoices):
    ACTOR = 'actor', _('actor')
    WRITER = 'writer', _('writer')
    DIRECTOR = 'director', _('director')


class FilmWorkType(models.TextChoices):
    MOVIE = 'film', _('film')
    SERIES = 'series', _('series')
    TV_SHOW = 'tv_show', _('tv_show')


class Person(TimeStampedModel):
    id = models.UUIDField('id', primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    full_name = models.TextField(_('Full name'))
    birth_date = models.DateField(_('Birth date'), null=True, default=None)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('Persons')
        db_table = 'content.person'

    def __str__(self):
        return self.full_name


class Genre(TimeStampedModel):
    id = models.UUIDField('id', primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.TextField(_('name'))
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        db_table = 'content.genre'

    def __str__(self):
        return self.name


class FilmWork(TimeStampedModel):
    id = models.UUIDField('id', primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    creation_date = models.DateField(_('Date of creation of film'), null=True, default=None)
    certificate = models.TextField(_('Certificate'), blank=True, null=True)
    file_path = models.FileField(_('File path'), upload_to='film_work/', null=True, default=None)
    rating = models.FloatField(_('Rating'), null=True, default=None)
    type = models.CharField(_('Type'), choices=FilmWorkType.choices, max_length=50, blank=True)
    mpaa_rating = models.CharField(_('MPAA film rating'), choices=MPAARatingType.choices, blank=True, max_length=50)
    genres = models.ManyToManyField('Genre', through='FilmWorkGenre')
    persons = models.ManyToManyField('Person', through='FilmWorkPerson')

    class Meta:
        verbose_name = _('Film')
        verbose_name_plural = _('Films')
        db_table = 'content.film_work'

    def __str__(self):
        return self.title


class FilmWorkPerson(TimeStampedModel):
    id = models.UUIDField('id', primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.CharField(_('Role'), choices=RoleType.choices, max_length=50)

    class Meta:
        verbose_name = _('Connection Film to Person')
        verbose_name_plural = _('Connections Film to Person')
        db_table = 'content.film_work_person'
        unique_together = ('film_work', 'person', 'role')


class FilmWorkGenre(TimeStampedModel):
    id = models.UUIDField('id', primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    film_work = models.ForeignKey(FilmWork, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Genre')
        verbose_name_plural = _('Genres')
        db_table = 'content.film_work_genre'
        unique_together = ('film_work', 'genre')
