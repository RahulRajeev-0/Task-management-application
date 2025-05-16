from django.urls import path
from . import views

urlpatterns = [
    path('management/', views.task_management_view, name='task_management'),
]
