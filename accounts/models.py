from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.managers import UserManager


class User(AbstractUser):
    """Custom user model that authenticates with email instead of username."""

    username = None
    email = models.EmailField("email address", unique=True)

    phone = models.CharField(max_length=20, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["phone"]

    objects = UserManager()

    def __str__(self):
        return self.email
