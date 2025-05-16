from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path("signup/", views.signup_view, name="signup"),
    path("logout/", views.logout_view, name="logout"),

    # jwt token urls
    path('api/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # endpoint to get user tasks
    path('api/user/tasks/', views.UserTaskView.as_view(), name='user_tasks'),
    path('api/user/tasks/<int:task_id>/', views.UserTaskView.as_view(), name='user_tasks'),

]
