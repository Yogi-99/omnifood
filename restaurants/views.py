from django.db.models import Count, Case, When
from django.shortcuts import render, redirect
from rest_framework import viewsets
from datetime import datetime, timedelta, timezone

from accounts.models import Courier
from restaurants.serializers import RestaurantSerializer, OrderSerializer
from .forms import UserEditForm
from .forms import RestaurantEditForm, MealForm
from .models import Meal, Order, Restaurant


# Create your views here.

# class ReadyOrdersViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.filter(status=Order.READY, courier=None).order_by('-id')
#     serializer_class = OrderSerializer


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
    today = datetime.now()
    revenue = []
    orders = []
    name = request.user.restaurant
    print("Restaurant: ", name)

    weekdays = [today - timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]
    print(today.weekday())
    print(0 - today.weekday())
    print(7 - today.weekday())
    print(today + timedelta(days=1))
    print(weekdays)

    for day in weekdays:
        delivered_orders = Order.objects.filter(
            restaurant=request.user.restaurant,
            status=Order.DELIVERED,
            created_at__year=day.year,
            created_at__month=day.month,
            created_at__day=day.day
        )
        revenue.append(sum(order.total for order in delivered_orders))
        orders.append(delivered_orders.count())

    return render(request, 'restaurants/report.html', {
        'revenue': revenue,
        'orders': orders,
        'restaurant_name': name
    })


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
    edit_meal_form = MealForm(instance=Meal.objects.get(id=id))

    if request.method == "POST":
        edit_meal_form = MealForm(request.POST, request.FILES, instance=Meal.objects.get(id=id))

        if edit_meal_form.is_valid():
            edit_meal_form.save()
            return redirect('meal')

    return render(request, 'restaurants/edit_meal.html', {
        'edit_meal_form': edit_meal_form
    })


class ListRestaurantsViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
