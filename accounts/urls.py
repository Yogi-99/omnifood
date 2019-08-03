from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views as user_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('home', user_views.home, name='home'),
    path('register', user_views.register, name='register'),
    path('auth', include('rest_framework_social_oauth2.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)