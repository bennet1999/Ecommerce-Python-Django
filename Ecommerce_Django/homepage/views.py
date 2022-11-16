from django.shortcuts import render
from product.models import Product
from category.models import Category,Subcategory

# Create your views here.
def index(request):

    featured = Product.objects.filter(is_featured=True)
    newarrivals = Product.objects.order_by('-created_date')[:9]

    category = Category.objects.order_by('name')
    sub_category = Subcategory.objects.order_by('name')

    context = {
        'category':category,
        'sub_category':sub_category,
        'featured':featured,
        'newarrivals':newarrivals
    }

    return render(request, 'user/index.html', context)