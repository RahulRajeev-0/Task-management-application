from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
import re


User = get_user_model()

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        # Handle login logic here
        pass
    return render(request, "login.html")


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get("username").strip()
        first_name = request.POST.get("first_name").strip()
        last_name = request.POST.get("last_name").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Basic validation
        if not all([username, first_name, last_name, password1, password2]):
            messages.error(request, "All fields are required.")
            return redirect('signup')

        if " " in username:
            messages.error(request, "Username cannot contain spaces.")
            return redirect('signup')

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect('signup')
        
        if password1.strip() == "":
            messages.error(request, "Password cannot be all spaces.")
            return render(request, 'signup.html')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        # Optional: You can use Django's built-in validators too

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password1,
        )
        messages.success(request, "Account created successfully. Please login.")
        return redirect('login')

    return render(request, "signup.html")
