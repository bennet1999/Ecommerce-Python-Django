from django.contrib import messages
from userProfile.models import Account
from cart.models import Coupon
from product.models import Product, Categoryoffer, Productoffer
from category.models import Category, Subcategory
from order.models import Order, OrderProduct, Payment
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.contrib.postgres.search import SearchVector
import datetime
from django.db.models import Sum

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
    delivered_orders = Order.objects.filter(status='Delivered')
    order_count = Order.objects.filter(status='Delivered').count()
    product_count = Product.objects.count()
    category_count = Category.objects.count()

    today = datetime.date.today()
    cm_delivered_orders = Order.objects.filter(status='Delivered',date__month=today.month)

    cod_sum = Order.objects.filter(status='Delivered',payment__method='COD').aggregate(Sum('total'))
    pyp_sum = Order.objects.filter(status='Delivered',payment__method='PYP').aggregate(Sum('total'))
    rzp_sum = Order.objects.filter(status='Delivered',payment__method='RZP').aggregate(Sum('total'))

    cod_order_count = Order.objects.filter(status='Delivered',payment__method='COD').count()
    pyp_order_count = Order.objects.filter(status='Delivered',payment__method='PYP').count()
    rzp_order_count = Order.objects.filter(status='Delivered',payment__method='RZP').count()

    category = Category.objects.all()

    c_order_count ={}
    for i in category:
        c_order_count[i.id] = OrderProduct.objects.filter(order__status='Delivered',product__category=i).count()
    

    revenue = 0
    for i in delivered_orders:
        revenue += i.total
    cm_revenue = 0
    for i in cm_delivered_orders:
        cm_revenue += i.total


    context = {
        'currentuser':currentuser,
        'revenue':revenue,
        'cm_revenue':cm_revenue,
        'order_count':order_count,
        'product_count':product_count,
        'category_count':category_count,
        'cod_sum':cod_sum,
        'rzp_sum':rzp_sum,
        'pyp_sum':pyp_sum,
        'cod_order_count':cod_order_count,
        'rzp_order_count':rzp_order_count,
        'pyp_order_count':pyp_order_count,
        'c_order_count':c_order_count,
        }
    return render(request, 'admin/admin_dashboard.html',context)

@login_required
def admin_user_list(request):
    currentuser = request.user
    if request.method =='POST':
        search = request.POST['search']

        obj = Account.objects.annotate(search=SearchVector('first_name', 'last_name', 'username','email','phone_number','id'),).filter(search=search,is_superuser=False, is_staff=False).order_by('id')

        paginator = Paginator(obj,20)
        page_number = request.GET.get('page')
        obj = paginator.get_page(page_number)

        context = {'obj':obj}
        return render(request, 'admin/admin_user_list.html', context)


    obj = Account.objects.filter(is_superuser=False, is_staff=False).order_by('id')

    paginator = Paginator(obj,5)
    page_number = request.GET.get('page')
    obj = paginator.get_page(page_number)


    context = {'currentuser':currentuser,'obj':obj}
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
    currentuser = request.user
    if request.method =='POST':
        search = request.POST['search']

        products = Product.objects.annotate(search=SearchVector('name', 'price', 'category__name','sub_category__name'),).filter(search=search).order_by('name')

        paginator = Paginator(products,20)
        page_number = request.GET.get('page')
        products = paginator.get_page(page_number)

        context = {'currentuser':currentuser,'products':products}
        return render(request, 'admin/admin-product-list.html', context)


    products = Product.objects.order_by('-created_date')

    paginator = Paginator(products,5)
    page_number = request.GET.get('page')
    products = paginator.get_page(page_number)

    context = {'currentuser':currentuser,'products':products}
    return render(request, 'admin/admin-product-list.html', context)

@login_required
def admin_delete_product(request,id):
    product = Product.objects.get(id=id)
    product.delete()
    return redirect('admin_product_list')

@login_required
def admin_add_product(request):
    currentuser = request.user
    category = Category.objects.all()
    sub_category = Subcategory.objects.all()
    context = { 'category':category, 'sub_category':sub_category, 'currentuser':currentuser}

    if request.method == 'POST':

            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']

            nonsizestock = request.POST['nonsizestock']
            sizestockS = request.POST['sizestockS']
            sizestockM = request.POST['sizestockM']
            sizestockL = request.POST['sizestockL']

            is_available = request.POST.getlist('is_available')
            is_available = True if is_available==[''] else False

            is_featured = request.POST.getlist('is_featured')
            is_featured = True if is_featured==[''] else False
            
            have_size = request.POST.getlist('have_size')
            have_size = True if have_size==[''] else False

            image1 = request.FILES.get('image1')
            image2 = request.FILES.get('image2')
            image3 = request.FILES.get('image3')
            image4 = request.FILES.get('image4')

            category = request.POST.get('category')
            category_instance = Category.objects.get(name=category)
         
            sub_category = request.POST.get('sub_category')   
            sub_category_instance = Subcategory.objects.get(name=sub_category)

            product = Product(name=name,description=description,price=price,nonsizestock=nonsizestock,sizestockS=sizestockS,sizestockM=sizestockM,sizestockL=sizestockL,is_available=is_available,is_featured=is_featured,have_size=have_size,category=category_instance,sub_category=sub_category_instance,image1=image1,image2=image2,image3=image3,image4=image4)
            product.save()
        
            messages.success(request,"Product Added Successfully")
            return redirect('admin_product_list')

    return render(request, 'admin/admin-add-product.html', context)


@login_required
def admin_edit_product(request,id):
    currentuser = request.user

    hcategory = Category.objects.all()
    hsub_category = Subcategory.objects.all()

    product = Product.objects.get(id=id)
    context = {'category':hcategory,'sub_category':hsub_category,'product':product,'currentuser':currentuser}

    if request.method == 'POST':

            name = request.POST['name']
            description = request.POST['description']
            price = request.POST['price']
            
            nonsizestock = request.POST['nonsizestock']
            sizestockS = request.POST['sizestockS']
            sizestockM = request.POST['sizestockM']
            sizestockL = request.POST['sizestockL']

            is_available = request.POST.getlist('is_available')
            is_available = True if is_available==[''] else False

            is_featured = request.POST.getlist('is_featured')
            is_featured = True if is_featured==[''] else False
            
            have_size = request.POST.getlist('have_size')
            have_size = True if have_size==[''] else False

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
            
            product.nonsizestock = nonsizestock
            product.sizestockS = sizestockS
            product.sizestockM = sizestockM
            product.sizestockL = sizestockL

            product.is_available = is_available
            product.is_featured = is_featured
            product.have_size = have_size
            
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


# -----------------------------------------------------------
# ------------------ CATEGORY  MANAGEMENT -------------------
# -----------------------------------------------------------

@login_required
def admin_category_management(request):
    currentuser = request.user

    category = Category.objects.all()
    sub_category = Subcategory.objects.all()

    context = { 'category':category,'sub_category':sub_category,'currentuser':currentuser }
    return render(request,'admin/admin-category-management.html',context)


@login_required
def admin_add_category(request):
    currentuser = request.user
    context = {'currentuser':currentuser}

    if request.method == 'POST':

            name = request.POST['name']
            description = request.POST['description']

            if not Category.objects.filter(name=name).exists():

                category = Category(name=name, description=description)
                category.save()

                messages.success(request,"Category Added Successfully")
                return redirect('admin_category_management')

            else:
                messages.success(request,"Category Name Already Exists")
                return redirect('admin_add_category')
                


    return render(request, 'admin/admin-add-category.html', context)



@login_required
def admin_delete_category(request, id):

    category = Category.objects.get(id=id)
    category.delete()
    messages.success(request,"Category Deleted Successfully")

    return redirect('admin_category_management')


@login_required
def admin_add_sub_category(request):
    currentuser = request.user

    hcategory = Category.objects.all()

    context = {'currentuser':currentuser,'category':hcategory}

    if request.method == 'POST':

            category = request.POST['category']
            name = request.POST['name']

            if not Subcategory.objects.filter(name=name).exists():

                category_instance = Category.objects.get(name=category)

                sub_category = Subcategory(category=category_instance,name=name)
                sub_category.save()

                messages.success(request,"Subcategory Added Successfully")
                return redirect('admin_category_management')

            else:
                messages.success(request,"Subcategory Name Already Exists")
                return redirect('admin_add_category')
                


    return render(request, 'admin/admin-add-sub-category.html', context)




@login_required
def admin_edit_category(request, id):

    currentuser = request.user
    category = Category.objects.get(id=id)
    
    context = {'currentuser':currentuser,'category':category}

    if request.method == 'POST':
        
        name = request.POST['name']
        description = request.POST['description']

        if not Category.objects.filter(name=name).exclude(name=category.name):
            category.name = name
            category.description = description
            category.save()
            messages.success(request,"Category Edited Successfully")
            return redirect('admin_category_management')
        else:
            messages.success(request,"Category Name Not Available")
            return redirect('admin_edit_category',category.id)

     
    return render(request,'admin/admin-edit-category.html',context)


@login_required
def admin_edit_sub_category(request,id):

    currentuser = request.user    

    sub_category = Subcategory.objects.get(id=id)

    context = {'currentuser':currentuser,'sub_category':sub_category}

    if request.method == 'POST':
        
        name = request.POST['name']

        if not Subcategory.objects.filter(name=name).exclude(name=sub_category.name):
            sub_category.name = name
            sub_category.save()
            messages.success(request,"Subcategory Edited Successfully")
            return redirect('admin_category_management')
        else:
            messages.success(request,"Subcategory Name Not Available")
            return redirect('admin_edit_sub_category',sub_category.id)

    return render(request,'admin/admin-edit-sub-category.html',context)

@login_required
def admin_delete_sub_category(request,id):
    
    sub_category = Subcategory.objects.get(id=id)
    sub_category.delete()
    
    messages.success(request,"Subcategory Deleted Successfully")
    
    return redirect('admin_category_management')



# -----------------------------------------------------------
# ------------------- ORDER  MANAGEMENT ---------------------
# -----------------------------------------------------------



def admin_order_list(request):
    currentuser = request.user
    if request.method =='POST':
        search = request.POST['search']

        orders = Order.objects.annotate(search=SearchVector('id', 'user__first_name', 'user__last_name'),).filter(search=search).order_by('-id')

        paginator = Paginator(orders,20)
        page_number = request.GET.get('page')
        orders = paginator.get_page(page_number)

        context = {'currentuser':currentuser,'orders':orders}
        return render(request,'admin/admin-order-list.html',context)


    orders = Order.objects.all().order_by('-id')

    paginator = Paginator(orders,8)
    page_number = request.GET.get('page')
    orders = paginator.get_page(page_number)

    context = {'currentuser':currentuser,'orders':orders}
    return render(request,'admin/admin-order-list.html',context)



def admin_order_details(request,id):
    currentuser = request.user
    order = Order.objects.get(id=id)
    order_items = OrderProduct.objects.filter(order=order)

    context = {'currentuser':currentuser,'order':order,'order_items':order_items}

    return render(request,'admin/admin-order-details.html',context)


def admin_order_change_status(request,id):

    if request.method == 'POST':

        order = Order.objects.get(id=id)
        order.status = request.POST.get('changeStatus')
        order.save()

        messages.success(request,"Status Changed Successfully")
        return HttpResponseRedirect(reverse('admin_order_details', kwargs={'id': id}))


# -----------------------------------------------------------
# ------------------- COUPON  MANAGEMENT --------------------
# -----------------------------------------------------------

@login_required
def admin_coupons(request):
    currentuser = request.user
    if request.method =='POST':
        search = request.POST['search']
        if search == '':
            return redirect('admin_coupons')

        coupons = Coupon.objects.annotate(search=SearchVector('code','percentage'),).filter(search=search).order_by('id')    

        paginator = Paginator(coupons,10)
        page_number = request.GET.get('page')
        coupons = paginator.get_page(page_number)

        context = {'coupons':coupons}
        return render(request, 'admin/admin-coupons.html', context)


    coupons = Coupon.objects.order_by('id')

    paginator = Paginator(coupons,10)
    page_number = request.GET.get('page')
    coupons = paginator.get_page(page_number)


    context = {'currentuser':currentuser,'coupons':coupons}
    return render(request, 'admin/admin-coupons.html', context)



@login_required
def admin_add_coupon(request):
    currentuser = request.user
    context = {'currentuser':currentuser}

    if request.method == 'POST':

            code = request.POST['code']
            percentage = request.POST['percentage']

            if not Coupon.objects.filter(code=code).exists():

                coupon = Coupon(code=code, percentage=percentage)
                coupon.save()

                messages.success(request,"Coupon Added Successfully")
                return redirect('admin_coupons')

            else:
                messages.success(request,"Coupon Code Already Exists")
                return redirect('admin_add_coupon')
                


    return render(request, 'admin/admin-add-coupon.html', context)


@login_required
def admin_delete_coupon(request, id):

    coupon = Coupon.objects.get(id=id)
    coupon.delete()
    messages.success(request,"Coupon Deleted Successfully")

    return redirect('admin_coupons')


@login_required
def admin_edit_coupon(request, id):

    currentuser = request.user
    coupon = Coupon.objects.get(id=id)
    
    context = {'currentuser':currentuser,'coupon':coupon}

    if request.method == 'POST':
        
        code = request.POST['code']
        percentage = request.POST['percentage']

        if not Coupon.objects.filter(code=code).exclude(code=coupon.code):
            coupon.code = code
            coupon.percentage = percentage
            coupon.save()
            messages.success(request,"Coupon Edited Successfully")
            return redirect('admin_coupons')
        else:
            messages.success(request,"Coupon Name Not Available")
            return redirect('admin_edit_coupon',coupon.id)

     
    return render(request,'admin/admin-edit-coupon.html',context)