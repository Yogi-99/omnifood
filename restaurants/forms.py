from accounts.forms import UserCreationForm, UserRegistrationForm
from django.contrib.auth.models import User
from django import forms
from .models import Restaurant, Meal


class UserEditForm(UserRegistrationForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )
        exclude = (
            'username',
            'password1',
            'password2',
        )


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name',
            'phone',
            'address',
            'logo'
        ]


class RestaurantEditForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = [
            'name',
            'phone',
            'address',
        ]
        exclude = (
            'logo',
        )


class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        exclude = ("restaurant",)
