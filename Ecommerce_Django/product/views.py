from django.shortcuts import render
from product.models import Product
from category.models import Category, Subcategory

def product_list(request,category,sub_category):

    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')

    if sub_category == 'None':
        products = Product.objects.filter(category__name=category)
        context = {'title':category,'products':products,'category':hcategory,'sub_category':hsub_category}
        return render(request,'user/shop-product-filter.html', context)
    else:
        products = Product.objects.filter(sub_category__name=sub_category)
        context = {'title':sub_category,'products':products,'category':hcategory,'sub_category':hsub_category}
        return render(request,'user/shop-product-filter.html', context)
    
    return render(request,'user/shop-product-filter.html')

def product_view(request,id):
    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')

    product = Product.objects.get(id=id)

    context = {'category':hcategory,'sub_category':hsub_category,'product':product}

    return render(request, 'user/shop-product-view.html',context)

