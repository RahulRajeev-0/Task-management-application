'''
User management 
- create user 
- delete user 
- assign user to admin or back to user 

'''
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from user.helper import validate_and_create_user
# Create your views here.

User = get_user_model()

@login_required
def admin_panel_home_view(request):
    if request.user.role not in ['ADMIN', 'SUPER_ADMIN']:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')
    
    if request.method == 'POST':
        success, result = validate_and_create_user(request, request.POST)
        if not success:
            messages.error(request, result)
            return redirect('home')
    users = User.objects.all()
    return render(request, "home.html", {"users": users})
