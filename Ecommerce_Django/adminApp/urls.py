from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin_user_list/', views.admin_user_list, name='admin_user_list'),
    path('block_unblock_user/', views.block_unblock_user, name='block_unblock_user'),
]