from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import UserLoginLogout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            UserLoginLogout.objects.create(user=user, login_time=timezone.now())
            return redirect('dashboard')
        else:
            error_message = "Invalid username or password"
    else:
        error_message = ""
    return render(request, 'login.html', {'error_message': error_message})

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def logout_view(request):
    UserLoginLogout.objects.filter(user=request.user, logout_time=None).update(logout_time=timezone.now())
    logout(request)
    return redirect('login')