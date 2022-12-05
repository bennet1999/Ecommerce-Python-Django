from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from userProfile.models import Account, Profile, Address
from category.models import Category, Subcategory
from order.models import Order, OrderProduct, Payment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .helper import MessageHandler
import random
from django.http import HttpResponseRedirect
from django.urls import reverse




def user_login(request):
    if 'email' in request.session:
        #return redirect('userprofile')
        return redirect('user_profile')
    else:
        if request.method == 'POST':
            email = request.POST['email']
            password = request.POST['password']

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request,user)
                request.session['email'] = email
                messages.info(request, 'Logged in Successfully')
                
                return redirect('user_profile')
                #return render(request, 'user/user-profile.html')
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('user_login')
        else:  
            return render(request, 'user/user-login.html')


def user_otp_request(request):
    if request.method == 'POST':
        phone_number = request.POST['phone_number']
        profile = Profile.objects.filter(phone_number = phone_number)
        if not profile.exists():
            messages.info(request, 'Phone Number Not Registered With')
            return redirect('user_login')
        else:
            profile1 = Profile.objects.get(phone_number=phone_number)
            otp = random.randint(1000,9999)

            while(Profile.objects.filter(otp=otp).exists()):
                otp = random.randint(1000,9999)

            profile.otp = otp
            profile1.save()
            messagehandler = MessageHandler(phone_number, profile1.otp)
            messagehandler.send_otp_via_message()

            messages.info(request, 'Otp Sent Successfully')

            context = {'phone_number':profile1.phone_number}            
            
            return render(request,'user/user-otp-login.html',context)
        


def user_otp_login(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        phone_number = request.POST['phone_number']
        profile = Profile.objects.get(phone_number=phone_number)
        if profile.otp == otp:
            login(request,profile.user)
            messages.info(request, 'Logged in Successfully')
            return redirect('user_profile')
        else:
            messages.info(request, 'Invalid OTP')
            return redirect('user_login')
    return redirect('user_login')

def user_register(request):
    if 'email' in request.session:
        return redirect('user_profile')
    else:
        if request.method == 'POST':

            username = request.POST['username']
            firstname = request.POST['firstname']
            lastname = request.POST['lastname']
            email = request.POST['email']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            phone_number = request.POST['phonenumber']

            if password1 == password2:
                if username == "":
                    messages.info(request, '! ! Username is Empty ! !')
                    return redirect('user_register')
                elif Account.objects.filter(username=username).exists():
                    messages.info(request, '! ! Username already exists ! !')
                    return redirect('user_register')
                elif Account.objects.filter(email=email).exists():
                    messages.info(request, '! ! Email already registered with ! !')
                    return redirect('user_register')
                elif not username.isalnum():
                    messages.info(request, '! ! Username must be Alpha-Numeric ! !')
                    return redirect('user_register')
                elif Account.objects.filter(phone_number=phone_number).exists():
                    messages.info(request, '! ! Phone number already registered with ! !')
                    return redirect('user_register')
                else:
                    user = Account.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password1,phone_number=phone_number)
                    profile = Profile.objects.create(user=user,phone_number=phone_number)
                    user.save()
                    profile.save()
                    messages.info(request, 'Your Account Has Been Successfully Created.')
                    return redirect('user_login')
            else:
                messages.info(request, "! ! Passwords not matching ! !")
                return redirect('user_register')
        else:
            return render(request, 'user/user-register.html')

def user_logout(request):
    if 'email' in request.session:
        request.session.flush()
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('user_login')

@login_required
def user_profile(request):
    currentuser = request.user
    user = Account.objects.get(email=currentuser)

    addresses = Address.objects.filter(user=user)

    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')

    orders = Order.objects.filter(user=user).order_by('-id')

    context = {'category':hcategory,'sub_category':hsub_category,'user':user,'addresses':addresses,'orders':orders}
    return render(request, 'user/user-profile.html', context)



def user_add_address(request):
    if request.method == 'POST':

            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            phone_number = request.POST['phone_number']
            email = request.POST['email']
            address = request.POST['address']
            town = request.POST['town']
            state = request.POST['state']
            pincode = request.POST['pincode']
            type = request.POST.get('type')
            
            currentuser = request.user
            user = Account.objects.get(email=currentuser)

            addressObj = Address.objects.create(first_name=first_name,last_name=last_name,phone_number=phone_number,email=email,address=address,town=town,state=state,pincode=pincode,type=type,user=user)
            addressObj.save()

            return redirect('user_profile')

def user_edit_address(request,id):
    if request.method == 'POST':

        addressObj = Address.objects.get(id=id)

        addressObj.first_name = request.POST['first_name']
        addressObj.last_name = request.POST['last_name']
        addressObj.phone_number = request.POST['phone_number']
        addressObj.email = request.POST['email']
        addressObj.address = request.POST['address']
        addressObj.town = request.POST['town']
        addressObj.state = request.POST['state']
        addressObj.pincode = request.POST['pincode']
        addressObj.type = request.POST.get('type')

        addressObj.save()

        return redirect('user_profile')

def user_delete_address(request,id):

    addressObj = Address.objects.get(id=id)
    addressObj.delete()

    return redirect('user_profile')

def user_order_details(request,id):
    hcategory = Category.objects.order_by('name')
    hsub_category = Subcategory.objects.order_by('name')

    order = Order.objects.get(id=id)

    order_items = OrderProduct.objects.filter(order=order)


    context = {'category':hcategory,'sub_category':hsub_category,'order':order,'order_items':order_items}
    return render(request,'user/user-order-details.html',context)


def user_order_cancel_return(request):
    if request.method =='POST':
        
        id = request.POST['order_id']
        order = Order.objects.get(id=id)
        
        roc = request.POST['roc']
        if roc == 'return':
            order.reason = request.POST['reasonReturn']
            order.status = 'Returned'
        elif roc == 'cancel':
            order.reason = request.POST['reasonCancel']
            order.status = 'Cancelled'
        
        order.save()
        
    return HttpResponseRedirect(reverse('user_order_details', kwargs={'id': id}))

def invoice(request):
    order = Order.objects.get(id=115)
    order_items = OrderProduct.objects.filter(order=order)
    context = {'order':order,'order_items':order_items}
    return render(request,'pdf/user_invoice.html',context)