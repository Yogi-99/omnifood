from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from restaurants.forms import RestaurantForm
from rest_framework import generics
from .models import Consumer, Courier
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .serializers import ConsumerSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from .permissions import UpdateOwnProfile
from rest_framework import viewsets


# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (UpdateOwnProfile, )


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ListCreateConsumer(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateConsumer(generics.ListCreateAPIView):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer


def register(request):
    user_form = UserRegistrationForm()
    restaurant_form = RestaurantForm()

    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        restaurant_form = RestaurantForm(request.POST, request.FILES)

        if user_form.is_valid() and restaurant_form.is_valid():
            new_user = user_form.save()
            new_restaurant = restaurant_form.save(commit=False)
            new_restaurant.user = new_user
            new_restaurant.save()

            login(request, authenticate(
                username=user_form.cleaned_data['username'],
                password=user_form.cleaned_data['password1']
            ))

            messages.success(request, f" Your account has been created. You can now login")
            return redirect('login')
    return render(request, 'accounts/register.html', {
        'user_form': user_form,
        'restaurant_form': restaurant_form
    })
