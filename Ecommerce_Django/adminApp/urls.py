from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_login, name='admin_login'),
    path('admin_logout', views.admin_logout, name='admin_logout'),
    path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),


    path('admin_user_list', views.admin_user_list, name='admin_user_list'),
    path('block_unblock_user/<int:id>', views.block_unblock_user, name='block_unblock_user'),


    path('admin_product_list', views.admin_product_list, name='admin_product_list'),
    path('admin_add_product', views.admin_add_product, name='admin_add_product'),
    path('admin_delete_product/<int:id>', views.admin_delete_product, name='admin_delete_product'),
    path('admin_edit_product/<int:id>', views.admin_edit_product, name='admin_edit_product'),


    path('admin_category_management', views.admin_category_management, name='admin_category_management'),
    path('admin_add_category', views.admin_add_category, name='admin_add_category'),
    path('admin_add_sub_category', views.admin_add_sub_category, name='admin_add_sub_category'),
    path('admin_edit_category/<int:id>', views.admin_edit_category, name='admin_edit_category'),
    path('admin_edit_sub_category/<int:id>', views.admin_edit_sub_category, name='admin_edit_sub_category'),
    path('admin_delete_category/<int:id>', views.admin_delete_category, name='admin_delete_category'),
    path('admin_edit_sub_category/admin_delete_sub_category/<int:id>', views.admin_delete_sub_category, name='admin_delete_sub_category'),
]