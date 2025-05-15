from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    # create user 
    def create_user(self, username, password=None, role='USER', **extra_fields):
        if not username:
            raise ValueError("Username is required")
        username = username.strip()
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # create super user
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('role', 'SUPER_ADMIN')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('USER', 'User'),
        ('ADMIN', 'Admin'),
        ('SUPER_ADMIN', 'Super Admin'),
    )

    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9_]+$',
        message='Username must contain only letters, numbers, and underscores.'
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': "This username is already taken.",
        }
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='USER')
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  

    def __str__(self):
        return f"{self.username} ({self.role})"
