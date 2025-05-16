from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import Task
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.

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



def edit_task_view(request, task_id):
    User = get_user_model()
    task = get_object_or_404(Task, id=task_id)

    # Permission check
    if request.user.role == 'ADMIN':
        if not (task.assigned_to and task.assigned_to.assigned_admin_id == request.user.id):
            messages.error(request, "You are not authorized to edit this task.")
            return redirect('task_management')
    elif request.user.role != 'SUPER_ADMIN':
        messages.error(request, "You are not authorized to edit this task.")
        return redirect('task_management')

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        assigned_to_id = request.POST.get('assigned_to')
        status = request.POST.get('status', 'PENDING')
        due_date = request.POST.get('due_date')
        description = request.POST.get('description', '')
        completion_report = request.POST.get('completion_report', '')
        worked_hours = request.POST.get('worked_hours', '')

        # Validate fields
        if not title or not assigned_to_id or not due_date:
            messages.error(request, 'All fields are required.')
            return redirect('task_management')

        try:
            assigned_to = User.objects.get(id=assigned_to_id)
        except User.DoesNotExist:
            messages.error(request, 'Assigned user does not exist.')
            return redirect('task_management')

        if assigned_to.role != 'USER':
            messages.error(request, 'You can only assign tasks to users.')
            return redirect('task_management')

        if request.user.role == 'ADMIN' and assigned_to.assigned_admin_id != request.user.id:
            messages.error(request, 'You can only assign tasks to your own users.')
            return redirect('task_management')

        # If status is completed, require completion_report and worked_hours
        if status == 'COMPLETED':
            if not completion_report or not worked_hours:
                messages.error(request, 'Completion report and worked hours are required for completed tasks.')
                return redirect('task_management')
            try:
                worked_hours_val = float(worked_hours)
            except ValueError:
                messages.error(request, 'Worked hours must be a number.')
                return redirect('task_management')
            task.completion_report = completion_report
            task.worked_hours = worked_hours_val
        else:
            task.completion_report = ''
            task.worked_hours = 0.0

        task.title = title
        task.assigned_to = assigned_to
        task.status = status
        task.due_date = due_date
        task.description = description
        task.save()
        messages.success(request, f'Task "{title}" updated successfully.')
        return redirect('task_management')

    # For GET (AJAX): return task data as JSON for modal
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'id': task.id,
            'title': task.title,
            'assigned_to': task.assigned_to.id if task.assigned_to else None,
            'status': task.status,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else '',
            'description': task.description,
            'completion_report': task.completion_report or '',
            'worked_hours': str(task.worked_hours) if task.worked_hours else '',
        })

    # fallback
    return redirect('task_management')

@require_POST
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # Only super admin or admin can delete
    if request.user.role == 'SUPER_ADMIN':
        pass  # allowed
    elif request.user.role == 'ADMIN':
        # Admin can only delete tasks of their assigned users
        if not (task.assigned_to and task.assigned_to.assigned_admin_id == request.user.id):
            messages.error(request, "You are not authorized to delete this task.")
            return redirect('task_management')
    else:
        messages.error(request, "You are not authorized to delete this task.")
        return redirect('task_management')

    task.delete()
    messages.success(request, f'Task "{task.title}" deleted successfully.')
    return redirect('task_management')



def task_detail_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Only super admin or admin (for their users) can view details
    if request.user.role == 'SUPER_ADMIN':
        pass
    elif request.user.role == 'ADMIN':
        if not (task.assigned_to and task.assigned_to.assigned_admin_id == request.user.id):
            messages.error(request, "You are not authorized to view this task.")
            return redirect('task_management')
    else:
        messages.error(request, "You are not authorized to view this task.")
        return redirect('task_management')
    return render(request, 'task_detail.html', {'task': task})