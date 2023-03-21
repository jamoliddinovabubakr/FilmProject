import json

from _decimal import Decimal
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from films.models import Film
from films.serializers import FilmSerializer


class FilmListAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass')
        self.client = APIClient()

        self.client.login(username='testuser', password='testpass')
        self.film_1 = Film.objects.create(name='Film 1', director='Director 1', price=2020)
        self.film_2 = Film.objects.create(name='Film 2', director='Director 2', price=2021)
        self.film_3 = Film.objects.create(name='Film 3', director='Director 3', price=2022)

    def test_get(self):
        url = reverse('film-list')

        access_token = AccessToken.for_user(self.user)
        # Include JWT token in Authorization header
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {str(access_token)}')

        response = self.client.get(url)
        serializer_data = FilmSerializer([self.film_1, self.film_2, self.film_3], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_filter(self):
        url = reverse('film-list')
        response = self.client.get(url, data={'price': 100.000})
        serializer_data = FilmSerializer([self.film_1, ], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_get_search(self):
        url = reverse('film-list')
        response = self.client.get(url, data={'search': 'director_1'})
        serializer_data = FilmSerializer([self.film_1, self.film_2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer_data, response.data)

    def test_create(self):
        self.assertEqual(3, Film.objects.all().count())
        url = reverse('film-list')
        data = {
            "name": "film 4",
            "director": "director 4",
            "price": '99.000'
        }
        json_data = json.dumps(data)
        response = self.client.post(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(4, Film.objects.all().count())

    def test_update(self):
        url = reverse('film-detail', args=(self.film_3.id,))
        data = {
            "name": self.film_3.name,
            "director": self.film_3.director,
            "price": '99.999'
        }
        json_data = json.dumps(data)
        response = self.client.put(url, data=json_data, content_type="application/json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.film_3.refresh_from_db()
        expected_price = Decimal("99.999")
        actual_price = self.film_3.price
        self.assertEqual(expected_price, actual_price)

    def test_delete(self):
        self.assertEqual(3, Film.objects.all().count())
        url = reverse('film-detail', args=(self.film_1.id,))
        response = self.client.delete(url, content_type="application/json")
        self.assertEqual(2, Film.objects.all().count())
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
