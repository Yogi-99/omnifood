from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='restaurant_logo', blank=True)

    def __str__(self):
        return self.name
