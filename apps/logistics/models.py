from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.utils.crypto import get_random_string

from apps.companies.models import Company
from apps.inventory.models import Item


def generate_order_number():
    # Must be defined here to avoid a circular import
    while True:
        order_number = "O-" + get_random_string(
            length=8, allowed_chars="BCDEFGHJKLMNPQRSTVWXZ1234567890"
        )
        if not Order.objects.filter(order_number=order_number).exists():
            return order_number


def generate_shipment_number():
    # Must be defined here to avoid a circular import
    while True:
        shipment_number = "S-" + get_random_string(
            length=8, allowed_chars="BCDEFGHJKLMNPQRSTVWXZ1234567890"
        )
        if not Shipment.objects.filter(
            shipment_number=shipment_number
        ).exists():
            return shipment_number


class Order(models.Model):
    order_number = models.CharField(
        max_length=10, default=generate_order_number, blank=False, unique=True
    )
    company = models.ForeignKey(
        Company,
        related_name="orders",
        on_delete=models.CASCADE,
    )

    items = models.ManyToManyField(
        Item, through="OrderItem", related_name="orders"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.order_number


class OrderItem(models.Model):
    item = models.ForeignKey(
        Item,
        related_name="order_items",
        on_delete=models.CASCADE,
        db_index=False,
    )
    order = models.ForeignKey(
        Order,
        related_name="order_items",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], blank=False
    )

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_updates",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "item",
                "order",
                name="unique_item_in_order",
                violation_error_message="This item is already in this order.",
            ),
            models.CheckConstraint(
                condition=Q(quantity__gte=1),
                name="order_item_quantity_gte_1",
                violation_error_message="Order item quantity must be at least 1.",
            ),
        ]

    def __str__(self):
        return f"{self.item.name} in Order {self.order.order_number} (Qty: {self.quantity})"


class Shipment(models.Model):
    shipment_number = models.CharField(
        max_length=10,
        default=generate_shipment_number,
        blank=False,
        unique=True,
    )
    company = models.ForeignKey(
        Company,
        related_name="shipments",
        on_delete=models.CASCADE,
    )

    items = models.ManyToManyField(
        Item, through="ShipmentItem", related_name="shipments"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return self.shipment_number


class ShipmentItem(models.Model):
    item = models.ForeignKey(
        Item,
        related_name="shipment_items",
        on_delete=models.CASCADE,
        db_index=False,
    )
    shipment = models.ForeignKey(
        Shipment,
        related_name="shipment_items",
        on_delete=models.CASCADE,
    )
    quantity = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], blank=False
    )

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="shipment_updates",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                "item",
                "shipment",
                name="unique_item_in_shipment",
                violation_error_message="This item is already in this shipment.",
            ),
            models.CheckConstraint(
                condition=Q(quantity__gte=1),
                name="shipment_item_quantity_gte_1",
                violation_error_message="Shipment item quantity must be at least 1.",
            ),
        ]

    def __str__(self):
        return f"{self.item.name} in Shipment {self.shipment.shipment_number} (Qty: {self.quantity})"
