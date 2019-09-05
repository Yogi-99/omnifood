from rest_framework import serializers
from .models import Consumer
from django.contrib.auth.models import User


class ConsumerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consumer
        fields = [
            'id',
            'user',
            'phone',
            'address',
        ]


class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
        ]
        extra_kwargs = {
            "password": {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        """Create and return a new User"""
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
