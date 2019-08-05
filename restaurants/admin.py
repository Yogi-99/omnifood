from django.contrib import admin
from .models import Restaurant, Meal, Order, OrderDetails

# Register your models here.

admin.site.register(Restaurant)
admin.site.register(OrderDetails)
admin.site.register(Meal)
admin.site.register(Order)
