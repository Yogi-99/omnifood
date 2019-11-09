from django.urls import path
from django.urls import include
from . import views as restaurant_views
from . import apis
from rest_framework.routers import DefaultRouter
from django.contrib import admin

router = DefaultRouter()
router.register('restaurants', restaurant_views.ListRestaurantsViewSet)
router.register('orders', apis.ReadyOrdersViewSet)

urlpatterns = [
    path('dashboard', restaurant_views.dashboard, name='dashboard'),
    path('account', restaurant_views.account, name='account'),
    path('order', restaurant_views.order, name='order'),
    path('report', restaurant_views.report, name='report'),
    path('meal', restaurant_views.meal, name='meal'),
    path('meal/add', restaurant_views.add_meal, name='add_meal'),
    path('api', apis.ListRestaurants.as_view(), name='list_restaurants'),
    path('meal/edit/<int:id>/', restaurant_views.edit_meal, name='edit_meal'),
    path('meals/<int:restaurant_id>', apis.ListMeals.as_view(), name='list_meal'),
    path('order/add/', apis.add_order),
    path('order/latest/', apis.get_latest_order),
    path('order/getorder/', apis.get_ready_orders),
    path('order/pick/', apis.pick_order),
    path('driver/latestorder/', apis.driver_latest_order),
    path('order/delivered/', apis.order_delivered),
    path('courier/revenue', apis.get_courier_revenue, name='courier_revenue'),

    path('check/order/', apis.check_order_add),

    path('', include(router.urls)),
    #    path('order/notification/<last_request_item>', apis.order_notification),
]
admin.site.site_header = 'Omnifood'
admin.site.index_title = 'Omnifood Administration'
