from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from oauth2_provider.models import AccessToken
from rest_framework.generics import ListAPIView
from datetime import datetime, timedelta
from accounts.models import Consumer
from .models import Restaurant, Meal, Order, OrderDetails
from django.utils import timezone
from .serializers import RestaurantSerializer, MealSerializer, OrderSerializer
from rest_framework import viewsets


class ListRestaurants(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class ReadyOrdersViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.filter(status=Order.READY, courier=None).order_by('-id')
    serializer_class = OrderSerializer


class ListRestaurantsViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class ListMeals(ListAPIView):
    serializer_class = MealSerializer

    def get_queryset(self):
        id = self.kwargs['restaurant_id']
        return Meal.objects.filter(restaurant_id=id)


def get_restaurant(request):
    restaurants = RestaurantSerializer(
        Restaurant.objects.all().order_by("-id"),
        many=True,
        context={
            'request': request
        }
    ).data

    return JsonResponse({
        'restaurants': restaurants
    })


def get_meals(request, restaurant_id):
    meals = MealSerializer(
        Meal.objects.filter(restaurant_id=restaurant_id).order_by("-id"),
        many=True,
        context={
            'request': request
        }
    ).data
    return JsonResponse({
        'meals': meals
    })


@csrf_exempt
def add_order(request):
    if request.method == "POST":
        token = Token.objects.get(key=request.POST.get('token'))
        consumer = token.user.consumer

        # consumer = Consumer.objects.get(user=request.POST.get('user'))

        if Order.objects.filter(consumer=consumer).exclude(status=Order.DELIVERED):
            return JsonResponse({
                'status': 'failed',
                'error': 'Your last order must be completed'
            })

        if not request.POST["address"]:
            return JsonResponse({
                'status': 'fail',
                'error': 'Address is required'
            })

        order_details = json.loads(request.POST['order_details'])

        order_total = 0

        for meal in order_details:
            order_total = Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]

        if len(order_details) > 0:
            order = Order.objects.create(
                consumer=consumer,
                restaurant_id=request.POST["restaurant_id"],
                total=order_total,
                status=Order.COOKING,
                address=request.POST['address']
            )

            for meal in order_details:
                OrderDetails.objects.create(
                    order=order,
                    meal_id=meal["meal_id"],
                    quantity=meal["quantity"],
                    sub_total=Meal.objects.get(id=meal["meal_id"]).price * meal["quantity"]
                )

            return JsonResponse({
                'status': 'success',
                'error': ''
            })


@csrf_exempt
def check_order_add(request):
    if request.method == "POST":
        token = Token.objects.get(key=request.POST.get('token'))
        consumer = token.user.consumer
        # consumer = Consumer.objects.get(user=request.POST.get("user"))

    if Order.objects.filter(consumer=consumer).exclude(status=Order.DELIVERED):
        return JsonResponse({
            'status': 'failed',
            'error': 'Your last order must be completed'
        })

    if not request.POST["address"]:
        return JsonResponse({
            'status': 'fail',
            'error': 'Address is required'
        })

    quantity = request.POST["quantity"]
    meal_id = Meal.objects.get(id=request.POST.get("meal_id"))
    # order_total = Meal.objects.get(id=meal_id).price * int(quantity)
    total = request.POST["total"]

    print(f'Total: {total}')
    print(f'Meal Id: {meal_id}')
    print(f'Meal Price: {type(meal_id.price)}')
    print(f'Meal Quantity: {quantity}')
    print(f'Meal Quantity Type: {type(quantity)}')

    order = Order.objects.create(
        consumer=consumer,
        restaurant_id=request.POST["restaurant_id"],
        total=total,
        status=Order.COOKING,
        address=request.POST["address"]
    )
    order_details = OrderDetails.objects.create(
        order=order,
        meal_id=meal_id.id,
        quantity=quantity,
        sub_total=total
    )
    print(meal_id)
    # print(meal_quantity)

    return JsonResponse({
        "status": "success"
    })


def get_latest_order(request):
    access_token = AccessToken.objects.get(token=request.GET.get("access_token"), expires__gt=timezone.now())

    consumer = access_token.user.consumer
    order = OrderSerializer(Order.objects.filter(consumer=consumer).last()).data
    return JsonResponse({
        'order': order
    })


def get_ready_orders(request):
    orders = OrderSerializer(
        Order.objects.filter(status=Order.READY, courier=None).order_by('-id'),
        many=True
    ).data

    return JsonResponse({
        'orders': orders
    })


@csrf_exempt
def pick_order(request):
    if request.method == 'POST':
        token = Token.objects.get(key=request.POST.get('token'))

        courier = token.user.courier

        if Order.objects.filter(courier=courier).exclude(status=Order.ONTHEWAY):
            return JsonResponse({
                'status': 'failed',
                'error': 'only one order at a time'
            })

        try:
            order = Order.objects.get(
                id=request.POST['order_id'],
                courier=None,
                status=Order.READY
            )

            order.courier = courier
            order.status = Order.ONTHEWAY
            order.picked_at = timezone.now()
            order.save()

            return JsonResponse({
                'status': 'success'
            })
        except Order.DoesNotExist:
            return JsonResponse({
                'status': 'failed',
                'error': 'order has picked up by another driver'
            })


def driver_latest_order(request):
    token = Token.objects.get(key=request.GET.get('token'))
    courier = token.user.courier

    order = OrderSerializer(
        Order.objects.filter(courier=courier).order_by('picked_at').last()
    ).data

    return JsonResponse({
        'order': order
    })


@csrf_exempt
def order_delivered(request):
    token = Token.objects.get(key=request.POST.get('token'))
    courier = token.user.courier

    order = Order.objects.get(id=request.POST['order_id'], courier=courier)
    order.status = Order.DELIVERED
    order.save()

    return JsonResponse({
        'status': 'delivered'
    })


def get_courier_revenue(request):
    revenue = {}
    today = timezone.now()

    token = Token.objects.get(key=request.GET.get('token'))
    courier = token.user.courier

    weekdays = [today + timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]

    for day in weekdays:
        orders = Order.objects.filter(
            courier=courier,
            status=Order.DELIVERED,
            created_at__year=day.year,
            created_at__month=day.month,
            created_at__day=day.day
        )

        revenue[day.strftime("%y %b %d")] = sum(order.total for order in orders)

    return JsonResponse({
        'revenue': revenue
    })

# def order_notification(request, last_request_time):
#     notification = Order.objects.filter(restaurant=request.user.restauramt, created_at__gt=last_request_time).count()
#     return JsonResponse({
#         "notification": notification
#     })
