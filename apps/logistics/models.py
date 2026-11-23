from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, F, Q, Sum, UniqueConstraint
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
    # Keep this or migrations break
    pass


class Order(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETE = "COMPLETE", "Complete"

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NEW
    )
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
        ordering = ["-created_at"]

    def __str__(self):
        return self.order_number

    def update_status(self):
        aggregates = self.order_items.aggregate(
            total=Sum("quantity_total"), picked=Sum("quantity_picked")
        )
        total_qty = aggregates["total"]
        picked_qty = aggregates["picked"]

        if picked_qty == total_qty:
            self.status = self.Status.COMPLETE
        else:
            self.status = self.Status.IN_PROGRESS

        self.save(update_fields=("status", "updated_at"))


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
    quantity_total = models.PositiveIntegerField(
        default=1, validators=[MinValueValidator(1)], blank=False
    )
    quantity_picked = models.PositiveIntegerField(default=0, blank=False)

    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_updates",
    )

    @property
    def remaining_qty(self):
        return self.quantity_total - self.quantity_picked

    class Meta:
        constraints = [
            UniqueConstraint(
                "item",
                "order",
                name="unique_item_in_order",
                violation_error_message="This item is already in this order.",
            ),
            CheckConstraint(
                condition=Q(quantity_total__gte=1),
                name="order_item_quantity_total_gte_1",
                violation_error_message=(
                    "Order item quantity_total must be at least 1."
                ),
            ),
            CheckConstraint(
                condition=Q(quantity_picked__lte=F("quantity_total")),
                name="quantity_picked_lte_quantity_total",
                violation_error_message=(
                    "Order item quantity_picked must less than or equal to"
                    " quantity_total."
                ),
            ),
        ]

    def __str__(self):
        return (
            f"{self.item.name} in Order {self.order.order_number} (Qty:"
            f" {self.quantity_total})"
        )
