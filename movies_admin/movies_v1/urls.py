from rest_framework import routers

from movies_v1.views.film_work import FilmWorkViewSet

router = routers.SimpleRouter()

router.register(r'movies', FilmWorkViewSet, basename='film_work')

urlpatterns = router.urls
