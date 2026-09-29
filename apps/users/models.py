from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.users.managers import CustomUserManager


class User(AbstractUser):
    """Custom User Model that removes all fields except email (now
    required) and password.
    """

    username = None
    first_name = None
    last_name = None
    email = models.EmailField(unique=True, verbose_name="email address")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
