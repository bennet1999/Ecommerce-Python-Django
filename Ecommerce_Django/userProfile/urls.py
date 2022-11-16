from django.urls import path
from . import views

urlpatterns = [
    path('user_login', views.user_login, name='user_login'),
    path('user_otp_request', views.user_otp_request, name='user_otp_request'),
    path('user_otp_login', views.user_otp_login, name='user_otp_login'),
    path('user_register', views.user_register, name='user_register'),
    path('user_profile', views.user_profile, name='user_profile'),
    path('user_logout', views.user_logout, name='user_logout'),
]