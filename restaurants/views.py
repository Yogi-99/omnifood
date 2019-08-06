from django.shortcuts import render, redirect
from .forms import UserEditForm
from .forms import RestaurantEditForm, MealForm
from .models import Meal, Order


# Create your views here.

def dashboard(request):
    return render(request, 'restaurants/dashboard.html')


def account(request):
    edit_user_form = UserEditForm(instance=request.user)
    edit_restaurant_form = RestaurantEditForm(instance=request.user.restaurant)

    if request.method == "POST":
        edit_user_form = UserEditForm(request.POST, instance=request.user)
        edit_restaurant_form = RestaurantEditForm(request.POST, instance=request.user.restaurant)

        if edit_user_form.is_valid() and edit_restaurant_form.is_valid():
            edit_user_form.save()
            edit_restaurant_form.save()

    return render(request, 'restaurants/account.html', {
        'edit_user_form': edit_user_form,
        'edit_restaurant_form': edit_restaurant_form
    })


def meal(request):
    meals = Meal.objects.filter(restaurant=request.user.restaurant).order_by("-id")
    return render(request, 'restaurants/meal.html', {
        'meals': meals
    })


def order(request):
    if request.method == "POST":
        order = Order.objects.get(id=request.POST['id'], restaurant=request.user.restaurant)
        if order.status == Order.COOKING:
            order.status = Order.READY
            order.save()

    orders = Order.objects.all() \
        .filter(restaurant=request.user.restaurant) \
        .order_by("-id")

    return render(request, 'restaurants/order.html', {
        'orders': orders
    })


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


def edit_meal(request, id):
    edit_meal_form = MealForm(instance = Meal.objects.get(id=id))

    if request.method == "POST":
        edit_meal_form = MealForm(request.POST, request.FILES, instance=Meal.objects.get(id = id))

        if edit_meal_form.is_valid():
            edit_meal_form.save()
            return redirect('meal')

    return render(request, 'restaurants/edit_meal.html', {
        'edit_meal_form': edit_meal_form
    })
