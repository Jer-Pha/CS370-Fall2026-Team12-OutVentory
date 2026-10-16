from django.conf import settings
from django.db import models
from django.db.models.functions import Lower

from apps.companies.models import Company


class Building(models.Model):
    name = models.CharField(max_length=100, blank=False)
    company = models.ForeignKey(
        Company,
        related_name="buildings",
        on_delete=models.CASCADE,
        db_index=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                "company",
                Lower("name"),
                name="unique_lower_building_name_in_company",
                violation_error_message="A building with this name already exists.",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class Item(models.Model):
    name = models.CharField(max_length=255, blank=False)
    company = models.ForeignKey(
        Company,
        related_name="items",
        on_delete=models.CASCADE,
        db_index=False,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                "company",
                Lower("name"),
                name="unique_lower_item_name_in_company",
                violation_error_message="An item with this name already exists.",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.company.name})"


class StorageLocation(models.Model):
    name = models.CharField(max_length=100, blank=False)
    building = models.ForeignKey(
        Building,
        related_name="locations",
        on_delete=models.CASCADE,
        db_index=False,
    )

    items = models.ManyToManyField(
        Item, through="InventoryLevel", related_name="locations"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(
                "building",
                Lower("name"),
                name="unique_lower_location_name_in_building",
                violation_error_message="A location with this name already exists.",
            ),
        ]

    def __str__(self):
        return f"{self.name} ({self.building.name})"


class InventoryLevel(models.Model):
    item = models.ForeignKey(
        Item,
        related_name="inventory_levels",
        on_delete=models.CASCADE,
        db_index=False,
    )
    location = models.ForeignKey(
        StorageLocation,
        related_name="inventory_levels",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(default=0, blank=False)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="inventory_updates",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "item",
                "location",
                name="unique_item_in_location",
                violation_error_message="This item is already in this location.",
            ),
        ]

    def __str__(self):
        return (
            f"{self.item.name} in {self.location.name} (Qty: {self.quantity})"
        )
