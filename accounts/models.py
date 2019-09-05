from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consumer')
    avatar = models.ImageField(upload_to='avatar')
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500)

    #
    # @receiver(post_save, sender=User)
    # def create_auth_token(self, instance=None, created=False, **kwargs):
    #     if created:
    #         Token.objects.create(user=instance)
    #
    def __str__(self):
        return self.user.get_full_name()


class Courier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='courier')
    avatar = models.ImageField(upload_to='avatar')
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=500)

    def __str__(self):
        return self.user.get_full_name()
