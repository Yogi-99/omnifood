from django.http import JsonResponse
from .models import Restaurant
from .serializers import RestaurantSerializer


def get_restaurant(request):
    restaurants = RestaurantSerializer(
        Restaurant.objects.all().order_by("-id"),
        many=True
    ).data

    return JsonResponse({
        'restaurants': restaurants
    })
