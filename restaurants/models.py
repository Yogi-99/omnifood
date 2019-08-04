from django.contrib.auth.models import User
from django.db import models


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='restaurant_logo', blank=False)

    def __str__(self):
        return self.name


class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    meal = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='meal_image/', blank=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.meal
