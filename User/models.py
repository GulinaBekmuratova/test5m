from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)

        user.save()

        return user

    def create_superuser(self, email, phone, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser have to be staff")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser have to be superuser")
        self.create_user(email, phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=80, unique=True)
    phone = models.CharField(max_length=13)
    is_active = models.BooleanField(default=True)  # Статус активации
    is_staff = models.BooleanField(default=False)  # Статус админа
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.email
