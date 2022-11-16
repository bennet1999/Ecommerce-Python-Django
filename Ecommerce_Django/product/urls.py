from django.urls import path
from . import views

urlpatterns = [
    path('product_list/<str:category>/<str:sub_category>/', views.product_list, name='product_list'),
]