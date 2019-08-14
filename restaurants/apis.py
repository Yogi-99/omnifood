from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.views import APIView
from oauth2_provider.models import AccessToken
from rest_framework.generics import ListAPIView
from .models import Restaurant, Meal, Order, OrderDetails
from django.utils import timezone
from .serializers import RestaurantSerializer, MealSerializer


class ListRestaurants(ListAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


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
        access_token = AccessToken.objects.get(token=request.POST.get("access_token"), expires__gt=timezone.now())
        consumer = access_token.user.consumer

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
                'status': 'success'
            })


def get_latest_order(request):
    return JsonResponse({

    })


# def order_notification(request, last_request_time):
#     notification = Order.objects.filter(restaurant=request.user.restauramt, created_at__gt=last_request_time).count()
#     return JsonResponse({
#         "notification": notification
#     })
