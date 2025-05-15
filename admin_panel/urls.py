from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel_home_view, name='home'),

]
