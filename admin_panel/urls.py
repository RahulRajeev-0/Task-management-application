from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel_home_view, name='home'),
    path('delete_user/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('toggle_user_role/<int:user_id>/', views.toggle_user_role_view, name='toggle_user_role'),  
]
