from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from restaurants.models import Order, OrderDetails
from restaurants.serializers import OrderSerializer


class GetOrdersListApiView(ListAPIView):
    queryset = Order.objects.filter(status=Order.READY)
    serializer_class = OrderSerializer
