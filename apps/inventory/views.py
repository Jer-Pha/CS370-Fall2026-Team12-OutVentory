from django.db.models import Prefetch
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import PageTitleMixin
from apps.inventory.forms import BuildingForm, ItemForm, StorageLocationForm
from apps.inventory.mixins import CompanyMixin, ProfilePermissionMixin
from apps.inventory.models import (
    Building,
    InventoryLevel,
    Item,
    StorageLocation,
)

############################### Building Views ################################


class BuildingBaseView(ProfilePermissionMixin, CompanyMixin, PageTitleMixin):
    permission_required = "is_owner"
    model = Building
    success_url = reverse_lazy("building_list")


class BuildingListView(BuildingBaseView, ListView):
    context_object_name = "buildings"
    paginate_by = 20
    page_title = "Buildings"
    template_name = "inventory/buildings/building_list.html"


class BuildingCreateView(BuildingBaseView, CreateView):
    form_class = BuildingForm
    page_title = "Add Building"
    template_name = "inventory/buildings/building_form.html"


class BuildingUpdateView(BuildingBaseView, UpdateView):
    form_class = BuildingForm
    template_name = "inventory/buildings/building_form.html"

    def get_page_title(self):
        return f"Edit Building: {self.object.name}"


class BuildingDeleteView(BuildingBaseView, DeleteView):
    template_name = "inventory/buildings/building_confirm_delete.html"

    def get_page_title(self):
        return f"Delete Building: {self.object.name}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        inventory_prefetch = Prefetch(
            "inventory_levels",
            queryset=InventoryLevel.objects.select_related("item").order_by(
                "-quantity", "item__name"
            ),
        )

        context["locations"] = self.object.locations.prefetch_related(
            inventory_prefetch
        )

        return context


################################# Item Views ##################################


class ItemBaseView(ProfilePermissionMixin, CompanyMixin, PageTitleMixin):
    model = Item
    success_url = reverse_lazy("item_list")


class ItemListView(ItemBaseView, ListView):
    permission_required = (
        "can_create_item",
        "can_edit_item",
        "can_delete_item",
    )
    permission_match_any = True
    context_object_name = "items"
    paginate_by = 20
    page_title = "Items"
    template_name = "inventory/items/item_list.html"


class ItemCreateView(ItemBaseView, CreateView):
    permission_required = "can_create_item"
    form_class = ItemForm
    page_title = "Add Item"
    template_name = "inventory/items/item_form.html"


class ItemUpdateView(ItemBaseView, UpdateView):
    permission_required = "can_edit_item"
    form_class = ItemForm
    template_name = "inventory/items/item_form.html"

    def get_page_title(self):
        return f"Edit Item: {self.object.name}"


class ItemDeleteView(ItemBaseView, DeleteView):
    permission_required = "can_delete_item"
    template_name = "inventory/items/item_confirm_delete.html"

    def get_page_title(self):
        return f"Delete Item: {self.object.name}"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["inventory_levels"] = (
            self.object.inventory_levels.select_related(
                "location__building"
            ).order_by(
                "-quantity", "location__building__name", "location__name"
            )
        )

        return context


############################### Location Views ################################


class LocationBaseView(ProfilePermissionMixin, CompanyMixin, PageTitleMixin):
    model = StorageLocation
    success_url = reverse_lazy("location_list")
    company_lookup = "building__company"


class LocationListView(LocationBaseView, ListView):
    permission_required = (
        "can_create_location",
        "can_edit_location",
        "can_delete_location",
    )
    permission_match_any = True
    context_object_name = "locations"
    paginate_by = 20
    page_title = "Locations"
    template_name = "inventory/locations/location_list.html"

    def get_queryset(self):
        return super().get_queryset().select_related("building")


class LocationCreateView(LocationBaseView, CreateView):
    permission_required = "can_create_location"
    form_class = StorageLocationForm
    page_title = "Add Location"
    template_name = "inventory/locations/location_form.html"


class LocationUpdateView(LocationBaseView, UpdateView):
    permission_required = "can_edit_location"
    form_class = StorageLocationForm
    template_name = "inventory/locations/location_form.html"

    def get_page_title(self):
        return f"Edit Location: {self.object.name}"


class LocationDeleteView(LocationBaseView, DeleteView):
    permission_required = "can_delete_location"
    template_name = "inventory/locations/location_confirm_delete.html"

    def get_page_title(self):
        return f"Delete Location: {self.object.name}"

    def get_queryset(self):
        return super().get_queryset().select_related("building")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["inventory_levels"] = (
            self.object.inventory_levels.select_related("item").order_by(
                "-quantity", "item__name"
            )
        )

        return context
