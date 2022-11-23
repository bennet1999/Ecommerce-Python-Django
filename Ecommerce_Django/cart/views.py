from django.shortcuts import render
from category.models import Category, Subcategory


def cart_view(request, id):
    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')
    context = {'category':hcategory,'sub_category':hsub_category}

    return render(request,'user/user-cart.html',context)