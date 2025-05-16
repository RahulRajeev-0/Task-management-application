from django.urls import path
from . import views

urlpatterns = [
    path('management/', views.task_management_view, name='task_management'),
    path('edit/<int:task_id>/', views.edit_task_view, name='edit_task'),
    path('delete/<int:task_id>/', views.delete_task_view, name='delete_task'),
    path('detail/<int:task_id>/', views.task_detail_view, name='task_detail'),
]
