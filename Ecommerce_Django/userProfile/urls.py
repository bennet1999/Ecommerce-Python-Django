from django.urls import path
from . import views

urlpatterns = [
    path('user_login', views.user_login, name='user_login'),
    path('user_otp_request', views.user_otp_request, name='user_otp_request'),
    path('user_otp_login', views.user_otp_login, name='user_otp_login'),
    path('user_register', views.user_register, name='user_register'),
    path('user_logout', views.user_logout, name='user_logout'),

    path('user_profile', views.user_profile, name='user_profile'),
    path('user_add_address', views.user_add_address, name='user_add_address'),
    path('user_delete_address/<int:id>', views.user_delete_address, name='user_delete_address'),

]