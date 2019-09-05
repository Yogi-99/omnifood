from django.contrib.auth.models import User
from accounts.models import Courier, Consumer
from django.utils import timezone
from django.db import models


class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=150)
    logo = models.ImageField(upload_to='restaurant_logo', blank=False)

    def __str__(self):
        return self.name


class Order(models.Model):
    COOKING = 1
    READY = 2
    ONTHEWAY = 3
    DELIVERED = 4

    STATUS_CHOICES = (
        (COOKING, "Cooking"),
        (READY, "Ready"),
        (ONTHEWAY, "On the way"),
        (DELIVERED, "Delivered"),
    )

    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE, null=True, blank=True)
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, null=True, blank=True)
    total = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    picked_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)


class Meal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='meal')
    meal = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='meal_image/', blank=False)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.meal


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return str(self.id)
