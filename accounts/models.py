from django.contrib.auth.models import User
from django.db import models


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consumer')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.user.get_full_name()


class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='courier')
    avatar = models.CharField(max_length=500)
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.user.get_full_name()
