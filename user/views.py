from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
import re
from django.contrib.auth import authenticate, login, logout
# helper
from .helper import validate_and_create_user, User


# login view 
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')  


# user signup view
def signup_view(request):
    if request.method == 'POST':
        success, result = validate_and_create_user(request, request.POST)
        if not success:
            messages.error(request, result)
            return redirect('signup')
        
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')
    return render(request, "signup.html")


# user logout (admin panel)
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')