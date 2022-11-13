from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
import logging



def admin_logout(request):
    if 'admin_username' in request.session:
        request.session.flush()
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('admin_login')


def admin_login(request):
    if 'admin_username' in request.session:
        return redirect('admin_dashboard')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None and user.is_superuser:
                login(request,user)
                request.session['admin_username'] = username
                messages.info(request, 'Logged in Successfully')
                currentuser = request.user
                return render(request, 'admin/admin_dashboard.html', {'currentuser':currentuser})
            else:
                messages.info(request, 'Invalid Credentials')
                return redirect('admin_login')
        else:  
            return render(request, 'admin/admin_login.html')

@login_required
def admin_dashboard(request):
    currentuser = request.user
    return render(request, 'admin/admin_dashboard.html',{'currentuser':currentuser})

def admin_user_list(request):
    obj = User.objects.filter(is_superuser=False, is_staff=False)
    context = {'obj':obj}
    return render(request, 'admin/admin_user_list.html', context)

def block_unblock_user(request):
        id=1
        x = User.objects.get(id = int(id))
        x.user_permissions.clear()
        return redirect('admin_user_list')


