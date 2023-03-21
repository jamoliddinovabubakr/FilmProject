from rest_framework.serializers import ModelSerializer
from films.models import Film


class FilmSerializer(ModelSerializer):
    class Meta:
        model = Film
        fields = ['name', 'director', 'price']
