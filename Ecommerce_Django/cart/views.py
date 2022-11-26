from django.shortcuts import render, redirect
from django.contrib import messages
from category.models import Category, Subcategory
from product.models import Product
from . models import CartItem
from django.http import JsonResponse

def add_to_cart(request,id):
    if 'email' in request.session:

        if request.method == 'POST':
            product = Product.objects.get(id=id)

            quantity = int(request.POST.get('quantity'))

            if product.have_size:
                size = request.POST['size']
            
            subtotal = product.price * quantity

            
            if product.have_size:
                if CartItem.objects.filter(product=product,size=size).exists():
                    cart_item = CartItem.objects.get(product=product,size=size)
                    cart_item.quantity += quantity
                    cart_item.subtotal = product.price * cart_item.quantity
                    cart_item.save()
                else:
                    cart_item = CartItem.objects.create(user=request.user,product=product,quantity=quantity,subtotal=subtotal,have_size=product.have_size,size=size)
                    cart_item.save()
            else:
                if CartItem.objects.filter(product=product).exists():
                    cart_item = CartItem.objects.get(product=product)
                    cart_item.quantity += quantity
                    cart_item.subtotal = product.price * cart_item.quantity
                    cart_item.save()
                else:
                    cart_item = CartItem.objects.create(user=request.user,product=product,quantity=quantity,subtotal=subtotal,have_size=product.have_size)
                    cart_item.save()

            return redirect('cart_view')

def add_quantity_cart_item(request,id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_view')

def subtract_quantity_cart_item(request,id):
    cart_item = CartItem.objects.get(id=id)
    cart_item.quantity -= 1
    cart_item.save()
    return redirect('cart_view')

def remove_from_cart(request,id):
    
    cart_item = CartItem.objects.get(id=id)
    cart_item.delete()
    
    messages.success(request,"Cart Item Removed Successfully")
    
    return redirect('cart_view')

def clear_cart(request):

    cart_items = CartItem.objects.filter(user=request.user)
    cart_items.delete()

    return redirect('cart_view')

def cart_view(request):
    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')

    cart_items = CartItem.objects.filter(user=request.user).order_by('-date_added')

    cart_total = 0
    for i in cart_items:
        cart_total += i.product.price * i.quantity

    context = {'category':hcategory,'sub_category':hsub_category,'cart_items':cart_items,'cart_total':cart_total}
    return render(request,'user/user-cart.html',context)

