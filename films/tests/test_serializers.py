from django.test import TestCase

from films.models import Film
from films.serializers import FilmSerializer


class FilmSerializerTestCase(TestCase):
    def test_ok(self):
        film_1 = Film.objects.create(name='film_1', director="director_1", price=100)
        film_2 = Film.objects.create(name='film_2', director="director_2", price=450.11)
        film_3 = Film.objects.create(name='film_3', director="director_3", price=123.42)
        data = FilmSerializer([film_1, film_2, film_3], many=True).data
        excepted_data = [
            {
                "name": 'film_1',
                "director": "director_1",
                "price": '100.000'
            },
            {
                "name": 'film_2',
                "director": "director_2",
                "price": '450.110'
            },
            {
                "name": 'film_3',
                "director": "director_3",
                "price": '123.420'
            },
        ]
        self.assertEqual(excepted_data, data)
