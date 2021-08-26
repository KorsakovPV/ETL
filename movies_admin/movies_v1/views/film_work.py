from rest_framework import viewsets

from movies_v1.filters.film_work import FilmWorkFilter
from movies_v1.models import FilmWork
from movies_v1.serializers.film_work import FilmWorkSerializer


class FilmWorkViewSet(viewsets.ModelViewSet):
    serializer_class = FilmWorkSerializer
    queryset = FilmWork.objects.all()
    filterset_class = FilmWorkFilter
