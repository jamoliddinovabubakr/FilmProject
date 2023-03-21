from django.db import models
from django.contrib.auth.models import User


class Film(models.Model):
    name = models.CharField(max_length=255)
    director = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name
