from rest_framework import serializers
from .models import (
    Restaurant,
    Meal,
    Consumer,
    Courier,
    Order,
    OrderDetails
)


class RestaurantSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    def get_logo(self, restaurant):
        request = self._context.get('request')
        logo_url = restaurant.logo.url
        return request.build_absolute_uri(logo_url)

    class Meta:
        model = Restaurant
        fields = (
            "id",
            "name",
            "phone",
            "address",
            "logo"
        )


class MealSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def get_image(self, meal):
        request = self.context.get('request')
        image_url = meal.image.url
        return request.build_absolute_uri(image_url)

    class Meta:
        model = Meal
        fields = [
            'id',
            'meal',
            'description',
            'image',
            'price'
        ]


class OrderConsumerSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user.get_full_name')

    class Meta:
        model = Consumer
        fields = [
            'id',
            'name',
            'phone',
            'address'
        ]


class OrderCourierSerializer(serializers.ModelSerializer):
    name = serializers.ReadOnlyField(source='user.get_full_name')

    class Meta:
        model = Courier
        fields = [
            'id',
            'name'
            'phone',
            'address'
        ]


class OrderRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            'id',
            'name',
            'phone',
            'address',
        ]


class OrderMealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = [
            'id',
            'name',
            'price'
        ]


class OrderDetailsSerializer(serializers.ModelSerializer):
    meal = OrderMealSerializer

    class Meta:
        model = OrderDetails
        fields = [
            'id',
            'meal',
            'quantity',
            'sub_total',
        ]


class OrderSerializer(serializers.ModelSerializer):
    consumer = OrderConsumerSerializer()
    courier = OrderCourierSerializer()
    restaurant = OrderRestaurantSerializer()
    order_details = OrderDetailsSerializer(many=True)
    status = serializers.ReadOnlyField(source='get_status_display')

    class Meta:
        model = Order
        fields = [
            'id',
            'consumer',
            'restaurant',
            'courier',
            'order_details',
            'total',
            'status',
            'address',

        ]
