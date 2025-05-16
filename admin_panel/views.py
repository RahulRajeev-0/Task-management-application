'''
User management 
- create user 
- delete user 
- assign user to admin or back to user 

'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from user.helper import validate_and_create_user
# Create your views here.

User = get_user_model()

# Admin panel User management views

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
        else:
            messages.success(request, f"User {result.username} created successfully.")
            return redirect('home')
        
    users = User.objects.all()
    return render(request, "home.html", {"users": users})


@login_required
def delete_user_view(request, user_id):
    if request.user.role != 'SUPER_ADMIN':
        messages.error(request, "Only Super Admin can perform this action.")
        return redirect('home')
    
    try:
        user = User.objects.get(id=user_id)
        if request.user == user:
            messages.error(request, "You cannot delete your own account.")
            return redirect('home')
        user.delete()
        messages.success(request, "User deleted successfully.")
    except User.DoesNotExist:
        messages.error(request, "User does not exist.")
    
    return redirect('home')


@login_required
def toggle_user_role_view(request, user_id):
    # Only super admin can make changes
    if request.user.role != 'SUPER_ADMIN':
        messages.error(request, "Only Super Admin can perform this action.")
        return redirect('home')

    # Prevent user from modifying themselves
    if request.user.id == user_id:
        messages.warning(request, "You cannot change your own role.")
        return redirect('home')

    user = get_object_or_404(User, id=user_id)

    if user.role == 'USER':
        user.role = 'ADMIN'
        messages.success(request, f"{user.username} has been promoted to Admin.")
    elif user.role == 'ADMIN':
        user.role = 'USER'
        messages.success(request, f"{user.username} has been demoted to User.")
    else:
        messages.warning(request, f"{user.username} is a Super Admin. No action taken.")
        return redirect('home')

    user.save()
    return redirect('home')


@login_required
def assign_admin_to_user(request, user_id):
    if request.user.role != 'SUPER_ADMIN':
        messages.error(request, "Access denied. Only Super Admins can assign users to admins.")
        return redirect('home')

    if request.method == "POST":
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, "The user you are trying to assign does not exist.")
            return redirect('home')

        admin_id = request.POST.get('assigned_admin_id')

        if not admin_id:
            messages.error(request, "Please select a valid admin from the list.")
            return redirect('home')

        # Check if the selected ID corresponds to an admin
        try:
            admin_user = User.objects.get(id=admin_id, role='ADMIN')
        except User.DoesNotExist:
            messages.error(request, "The selected admin does not exist or is not an admin.")
            return redirect('home')

        # Only normal users should be assigned
        if user.role != 'USER':
            messages.error(request, "Only users with the role 'USER' can be assigned to admins.")
            return redirect('home')

        # Prevent reassigning to the same admin
        if user.assigned_admin == admin_user:
            messages.info(request, f"User {user.username} is already assigned to Admin {admin_user.username}.")
            return redirect('home')

        # Assign the user
        user.assigned_admin = admin_user
        user.save()
        messages.success(request, f"Successfully assigned {user.username} to Admin {admin_user.username}.")

    return redirect('home')