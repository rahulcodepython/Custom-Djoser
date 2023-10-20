from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from . import manager as self_manager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=254)
    first_name = models.CharField(max_length=1000, blank=True)
    last_name = models.CharField(max_length=1000, blank=True)
    username = models.CharField(max_length=1000, blank=True)
    # password .....

    is_staff = models.BooleanField(default=True)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = None
    user_permissions = None
    last_login = None

    objects = self_manager.UserManager()

    REQUIRED_FIELDS = ['first_name', 'last_name']

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['email']

    def __str__(self) -> str:
        return self.email


class ActivationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=1000)
    token = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Activation Code'
        verbose_name_plural = 'Activation Codes'

    def __str__(self) -> str:
        return self.user.email


class ResetPasswordCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uid = models.CharField(max_length=1000)
    token = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Reset Password Code'
        verbose_name_plural = 'Reset Password Codes'

    def __str__(self) -> str:
        return self.user.email
