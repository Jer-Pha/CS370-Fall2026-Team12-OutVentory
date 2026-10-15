# from apps.companies.models import Company
from django.conf import settings
from django.db import models


class UserProfile(models.Model):
    # Core
    first_name = models.CharField(max_length=100, blank=False)
    last_name = models.CharField(max_length=100, blank=False)
    is_admin = models.BooleanField(default=False, null=False, db_index=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name="profile",
        on_delete=models.CASCADE,
    )
    # company = models.ForeignKey(
    #     Company, related_name="employees", on_delete=models.CASCADE
    # )

    # Permissions
    can_pick_item = models.BooleanField(
        default=False, null=False, db_index=True
    )
    can_pick_order = models.BooleanField(
        default=False, null=False, db_index=True
    )
    can_store_item = models.BooleanField(
        default=False, null=False, db_index=True
    )
    can_store_delivery = models.BooleanField(
        default=False, null=False, db_index=True
    )
    can_create_item = models.BooleanField(
        default=False, null=False, db_index=True
    )
    can_edit_item = models.BooleanField(
        default=False, null=False, db_index=True
    )
    can_delete_item = models.BooleanField(
        default=False, null=False, db_index=True
    )
    can_create_location = models.BooleanField(
        default=False, null=False, db_index=True
    )
    can_edit_location = models.BooleanField(
        default=False, null=False, db_index=True
    )
    can_delete_location = models.BooleanField(
        default=False, null=False, db_index=True
    )

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
