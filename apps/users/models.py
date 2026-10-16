from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.companies.models import Company
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


class EmployeeProfile(models.Model):
    """Non-authentication user settings"""

    # Basic Info
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)

    # Relationships
    user = models.OneToOneField(
        User,
        related_name="profile",
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        Company, related_name="employees", on_delete=models.CASCADE
    )

    # Roles
    is_admin = models.BooleanField(default=False, null=False)
    is_owner = models.BooleanField(default=False, null=False)

    # Permissions
    can_pick_item = models.BooleanField(default=False, null=False)
    can_pick_order = models.BooleanField(default=False, null=False)
    can_store_item = models.BooleanField(default=False, null=False)
    can_store_delivery = models.BooleanField(default=False, null=False)
    can_create_item = models.BooleanField(default=False, null=False)
    can_edit_item = models.BooleanField(default=False, null=False)
    can_delete_item = models.BooleanField(default=False, null=False)
    can_create_location = models.BooleanField(default=False, null=False)
    can_edit_location = models.BooleanField(default=False, null=False)
    can_delete_location = models.BooleanField(default=False, null=False)

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def name_short(self):
        return f"{self.first_name} {self.last_name[0]}."

    def __str__(self):
        return f"{self.name} ({self.company.name})"
