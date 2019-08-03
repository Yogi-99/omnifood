from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserRegistrationForm, RestaurantForm
from django.contrib.auth import authenticate, login


# Create your views here.

def home(request):
    return render(request, 'accounts/home.html')


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
