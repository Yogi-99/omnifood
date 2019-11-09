from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from restaurants.models import Order, OrderDetails
from restaurants.serializers import OrderSerializer
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from oauth2_provider.models import AccessToken
from .models import Courier


class GetOrdersListApiView(ListAPIView):
    queryset = Order.objects.filter(status=Order.READY, courier=None)
    serializer_class = OrderSerializer


@csrf_exempt
def consumer_location(request):
    if request.method == "POST":
        token = Token.objects.get(key=request.POST.get('token'))
        consumer = token.user.consumer

        consumer.latitude = request.POST['latitude']
        consumer.longitude = request.POST['longitude']
        consumer.save()

        return JsonResponse({
            'status': 'success',
            'error': ''
        })


@csrf_exempt
def get_consumer_location(request):
    consumer = request.user.consumer.get(id=request['id'])
    print('Consumer: ', consumer)


@csrf_exempt
def courier_location(request):
    if request.method == "POST":
        token = Token.objects.get(key=request.POST.get('token'))
        courier = token.user.courier

        courier.location = request.POST['location']
        courier.save()

        return JsonResponse({
            'status': 'success',
            'error': ''
        })


def get_courier_location(request):
    token = Token.objects.get(key=request.GET.get('token'))
    consumer = token.user.consumer

    current_order = Order.objects.filter(
        consumer=consumer,
        status=Order.ONTHEWAY,
    ).last()

    location = current_order.courier.location

    return JsonResponse({
        'location': location
    })

# @csrf_exempt
# def pick_order(request):
#     if request.method == "POST":
#         access_token = AccessToken.objects.get(token=request.POST.get("access_token"), expires__gt=timezone.now())
#
#         courier = access_token.user.courier
#
#         # courier = Courier.objects.get(user=request.POST['c_id'])
#         if Order.objects.filter(courier=courier).exclude(status=Order.ONTHEWAY):
#             return JsonResponse({
#                 'status': 'failed',
#                 'error': 'You can only pick one order at a time'
#             })
#         try:
#             order = Order.objects.get(
#                 id=request.POST['order_id'],
#                 courier=None,
#                 status=Order.READY
#             )
#             order.courier = courier
#             order.status = Order.ONTHEWAY
#             order.picked_at = timezone.now()
#             order.save()
#
#             return JsonResponse({
#                 'status': 'success'
#             })
#
#         except Order.DoesNotExist:
#             return JsonResponse({
#                 'status': 'failed',
#                 'error': 'This order has been picked up by another driver'
#             })
