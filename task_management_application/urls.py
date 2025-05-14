
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-role-auth/', include('user_role_auth.urls'))
]
