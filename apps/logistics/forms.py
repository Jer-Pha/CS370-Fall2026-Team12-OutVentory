from django import forms
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from apps.inventory.models import InventoryLevel, StorageLocation


class OrderItemPickForm(forms.Form):
    location = forms.ModelChoiceField(
        queryset=StorageLocation.objects.none(),
        empty_label="Select a Location",
    )
    quantity = forms.IntegerField(
        min_value=1,
        label="Quantity",
        help_text="Enter the number of units to pick.",
    )

    def __init__(self, *args, instance=None, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance
        self.item = None
        self.company = company

        if self.instance:
            self.item = self.instance.item

        if company:
            self.fields["location"].queryset = (
                StorageLocation.objects
                # .select_related("building")
                .filter(building__company=company)
                .filter(
                    inventory_levels__item=self.item,
                    inventory_levels__quantity__gte=1,
                )
                .distinct()
                .order_by("building__name", "name")
            )

    def clean_quantity(self):
        location = self.cleaned_data.get("location")
        pick_quantity = self.cleaned_data.get("quantity", 0)
        self.inventory_instance = get_object_or_404(
            InventoryLevel, item=self.item, location=location
        )
        loc_quantity = self.inventory_instance.quantity

        if pick_quantity > loc_quantity:
            raise ValidationError(
                f"Cannot pick {pick_quantity} units. Only {loc_quantity} available"
                " in this location."
            )
        if self.instance and pick_quantity > self.instance.remaining_qty:
            raise ValidationError(
                f"Cannot pick {pick_quantity} units. Only"
                f" {self.instance.remaining_qty} units are needed."
            )
        return pick_quantity
