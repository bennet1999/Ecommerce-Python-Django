from django.shortcuts import render
from product.models import Product
from category.models import Category, Subcategory
from django.core.paginator import Paginator


def product_list(request,category,sub_category,sortby):

    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')

    if sortby == 'relevance':
        sortby = 'name'
    elif sortby == 'newest':
        sortby = '-created_date'
    elif sortby == 'lowtohigh':
        sortby = 'price'
    elif sortby == 'hightolow':
        sortby = '-price'


    if sub_category == 'None':
        products = Product.objects.filter(category__name=category).order_by(sortby)

        paginator = Paginator(products,6)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        context = {'title':category,'products':products,'category':hcategory,'sub_category':hsub_category,'currentCat':category,'currentSubcat':sub_category}
    else:
        products = Product.objects.filter(sub_category__name=sub_category).order_by(sortby)

        paginator = Paginator(products,6)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        context = {'title':sub_category,'products':products,'category':hcategory,'sub_category':hsub_category,'currentCat':category,'currentSubcat':sub_category}
    
    return render(request,'user/shop-product-filter.html', context)

def product_view(request,id):
    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')

    product = Product.objects.get(id=id)

    context = {'category':hcategory,'sub_category':hsub_category,'product':product}

    return render(request, 'user/shop-product-view.html',context)

