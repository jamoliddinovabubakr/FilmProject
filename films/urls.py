from django.urls import path
from rest_framework.routers import SimpleRouter
from films.views import FilmViewSet

router = SimpleRouter()
router.register(r'film', FilmViewSet)

urlpatterns = [

]

urlpatterns += router.urls
