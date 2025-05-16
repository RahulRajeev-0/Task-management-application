from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import re
from django.contrib.auth import authenticate, login, logout
# helper
from .helper import validate_and_create_user, User

# models 
from tasks.models import Task

# serializers
from .serializers import TaskSerializer


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


# handle user tasks related logic
class UserTaskView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # update task status
    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({"error": "Task not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
