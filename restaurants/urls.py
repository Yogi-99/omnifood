from django.urls import path
from . import views as restaurant_views
from . import apis

urlpatterns = [
    path('dashboard', restaurant_views.dashboard, name='dashboard'),
    path('account', restaurant_views.account, name='account'),
    path('order', restaurant_views.order, name='order'),
    path('report', restaurant_views.report, name='report'),
    path('meal', restaurant_views.meal, name='meal'),
    path('meal/add', restaurant_views.add_meal, name='add_meal'),
    path('api', apis.get_restaurant)
]