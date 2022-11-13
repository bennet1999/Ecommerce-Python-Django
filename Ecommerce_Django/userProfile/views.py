from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from userProfile.models import Account



def user_login(request):
    return render(request, 'user/user-login.html')

def user_register(request):
    if 'username' in request.session:
        return redirect('index')
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
                    userobj =Account.objects.create_user(username=username,first_name=firstname,last_name=lastname,email=email,password=password1,phone_number=phone_number)
                    userobj.save()
                    messages.info(request, 'Your Account Has Been Successfully Created.')
                    return redirect('user_login')
            else:
                messages.info(request, "! ! Passwords not matching ! !")
                return redirect('user_register')
        else:
            return render(request, 'user/user-register.html')

def user_logout(request):
    pass