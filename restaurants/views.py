from django.shortcuts import render, redirect
from .forms import UserEditForm
from .forms import RestaurantForm, MealForm


# Create your views here.

def dashboard(request):
    return render(request, 'restaurants/dashboard.html')


def account(request):
    edit_user_form = UserEditForm(instance=request.user)
    edit_restaurant_form = RestaurantForm(instance=request.user.restaurant)

    return render(request, 'restaurants/account.html', {
        'edit_user_form': edit_user_form,
        'edit_restaurant_form': edit_restaurant_form
    })


def meal(request):
    return render(request, 'restaurants/meal.html')


def order(request):
    return render(request, 'restaurants/order.html')


def report(request):
    return render(request, 'restaurants/report.html')


def add_meal(request):
    meal_form = MealForm()

    if request.method == "POST":
        meal_form = MealForm(request.POST, request.FILES)

        if meal_form.is_valid():
            meal_object = meal_form.save(commit=False)
            meal_object.restaurant = request.user.restaurant
            meal_object.save()
            return redirect('meal')

    return render(request, 'restaurants/add_meal.html', {
        'meal_form': meal_form
    })
