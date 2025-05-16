from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Task
from django.utils import timezone

# Create your views here.


# create task 

# listing all tasks

User = get_user_model()

def task_management_view(request):
    if request.user.role not in ['ADMIN', 'SUPER_ADMIN']:
        messages.error(request, "You are not authorized to view this page.")
        return redirect('login')

    # Handle task creation
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        assigned_to_id = request.POST.get('assigned_to')
        status = request.POST.get('status', 'PENDING')
        due_date = request.POST.get('due_date')
        description = request.POST.get('description', '')

        # Validate fields
        if not title or not assigned_to_id or not due_date:
            messages.error(request, 'All fields are required.')
            return redirect('task_management')

        try:
            assigned_to = User.objects.get(id=assigned_to_id)
        except User.DoesNotExist:
            messages.error(request, 'Assigned user does not exist.')
            return redirect('task_management')

        # Only allow assignment to users (not admins/superadmins)
        if assigned_to.role != 'USER':
            messages.error(request, 'You can only assign tasks to users.')
            return redirect('task_management')

        # Admins can only assign to their own users
        if request.user.role == 'ADMIN' and assigned_to.assigned_admin_id != request.user.id:
            messages.error(request, 'You can only assign tasks to your own users.')
            return redirect('task_management')

        # Super admin can assign to any user
        task = Task.objects.create(
            title=title,
            assigned_to=assigned_to,
            status=status,
            due_date=due_date,
            description=description
        )
        messages.success(request, f'Task "{title}" created and assigned to {assigned_to.username}.')
        return redirect('task_management')

    # List tasks
    if request.user.role == 'SUPER_ADMIN':
        tasks = Task.objects.all().order_by('-created_at')
        users = User.objects.filter(role='USER')
    elif request.user.role == 'ADMIN':
        users = User.objects.filter(role='USER', assigned_admin=request.user)
        tasks = Task.objects.filter(assigned_to__in=users).order_by('-created_at')
    else:
        tasks = Task.objects.none()
        users = User.objects.none()

    return render(request, 'task_management.html', {'tasks': tasks, 'users': users})