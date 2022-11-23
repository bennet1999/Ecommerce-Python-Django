from django.urls import path
from . import views

urlpatterns = [
    path('cart_view/<int:id>', views.cart_view, name='cart_view')
]