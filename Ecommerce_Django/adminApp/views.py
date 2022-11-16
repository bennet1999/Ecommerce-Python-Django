from django.contrib import messages
from userProfile.models import Account
from product.models import Product, Categoryoffer, Productoffer
from category.models import Category, Subcategory
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout


def admin_logout(request):
    if 'admin_username' in request.session:
        request.session.flush()
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('admin_login')


def admin_login(request):
    if 'admin_email' in request.session:
        return redirect('admin_dashboard')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user is not None and user.is_superuser:
                login(request,user)
                request.session['admin_email'] = email
                messages.info(request, 'Logged in Successfully')
                return redirect(admin_dashboard)
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('admin_login')
        else:  
            return render(request, 'admin/admin_login.html')

@login_required
def admin_dashboard(request):
    currentuser = request.user
    return render(request, 'admin/admin_dashboard.html',{'currentuser':currentuser})

@login_required
def admin_user_list(request):
    obj = Account.objects.filter(is_superuser=False, is_staff=False).order_by('id')
    context = {'obj':obj}
    #currentuser = request.user
    return render(request, 'admin/admin_user_list.html', context)

@login_required
def block_unblock_user(request,id):
        x=Account.objects.get(id=id)
        if x.is_active:
            x.is_active=False

        else:
            x.is_active=True
    
        x.save()         
        return redirect('admin_user_list')


# -----------------------------------------------------------
# ------------------ PRODUCT MANAGEMENT ---------------------
# -----------------------------------------------------------

@login_required
def admin_product_list(request):
    products = Product.objects.order_by('-created_date')
    context = {'products':products}
    return render(request, 'admin/admin-product-list.html', context)

@login_required
def admin_delete_product(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('admin_product_list')

@login_required
def admin_add_product(request):

    category = Category.objects.all()
    sub_category = Subcategory.objects.all()
    context = { 'category':category, 'sub_category':sub_category }

    if request.method == 'POST':

            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            stock = request.POST['stock']

            is_available = request.POST.getlist('is_available')
            is_available = True if is_available==[''] else False

            is_featured = request.POST.getlist('is_featured')
            is_featured = True if is_featured==[''] else False
            
            have_size = request.POST.getlist('have_size')
            have_size = True if have_size==[''] else False

            size = request.POST.get('size')

            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            image4 = request.FILES.get('image4')

            category = request.POST.get('category')
            category_instance = Category.objects.get(name=category)
         
            sub_category = request.POST.get('sub_category')   
            sub_category_instance = Subcategory.objects.get(name=sub_category)

            product = Product(name=name,description=description,price=price,stock=stock,is_available=is_available,is_featured=is_featured,have_size=have_size,size=size,category=category_instance,sub_category=sub_category_instance,image1=image1,image2=image2,image3=image3,image4=image4)
            product.save()
        
            messages.success(request,"Product Added Successfully")
            return redirect('admin_product_list')

    return render(request, 'admin/admin-add-product.html', context)


@login_required
def admin_edit_product(request,id):

    hcategory = Category.objects.all()
    hsub_category = Subcategory.objects.all()

    product = Product.objects.get(id=id)
    context = {'category':hcategory,'sub_category':hsub_category,'product':product}

    if request.method == 'POST':

            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            stock = request.POST['stock']

            is_available = request.POST.getlist('is_available')
            is_available = True if is_available==[''] else False

            is_featured = request.POST.getlist('is_featured')
            is_featured = True if is_featured==[''] else False
            
            have_size = request.POST.getlist('have_size')
            have_size = True if have_size==[''] else False

            size = request.POST.get('size')

            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            image4 = request.FILES.get('image4')

            category = request.POST.get('category')
            category_instance = Category.objects.get(name=category)
         
            sub_category = request.POST.get('sub_category')   
            sub_category_instance = Subcategory.objects.get(name=sub_category)

            product.name = name
            product.description = description
            product.price = price
            product.stock = stock
            product.is_available = is_available
            product.is_featured = is_featured
            product.have_size = have_size
            product.size = size
            
            if image1 != None:
                product.image1 = image1
            if image2 != None:
                product.image2 = image2
            if image3 != None:
                product.image3 = image3
            if image4 != None:
                product.image4 = image4

            product.category = category_instance
            product.sub_category = sub_category_instance

            product.save()
            return redirect('admin_product_list')


    return render(request,'admin/admin-edit-product.html',context)

