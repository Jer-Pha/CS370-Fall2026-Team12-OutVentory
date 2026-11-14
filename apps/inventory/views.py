from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    FormView,
    ListView,
    UpdateView,
)

from apps.core.mixins import PageTitleMixin
from apps.inventory.forms import (
    BuildingForm,
    InventoryAdjustForm,
    ItemForm,
    StorageLocationForm,
    StoreNewInventoryForm,
)
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


############################ Inventory Management #############################


class InventoryListView(
    LoginRequiredMixin, CompanyMixin, PageTitleMixin, ListView
):
    """Displays existing inventory (quantity > 0) scoped to the user's company."""

    model = InventoryLevel
    company_lookup = "item__company"
    context_object_name = "inventory_levels"
    paginate_by = 20
    page_title = "View Inventory"
    template_name = "inventory/manage_inventory/inventory_list.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(quantity__gt=0)
            .select_related("item", "location__building")
            .order_by(
                "location__building__name",
                "location__name",
                "item__name",
            )
        )


class InventoryAdjustBaseView(
    ProfilePermissionMixin, CompanyMixin, PageTitleMixin, UpdateView
):
    """Base view for adjusting quantity on an existing InventoryLevel record."""

    model = InventoryLevel
    permission_required = (
        "can_pick_item",
        "can_store_item",
    )
    permission_match_any = True
    form_class = InventoryAdjustForm
    template_name = "inventory/manage_inventory/inventory_adjust_form.html"
    success_url = reverse_lazy("inventory_list")
    company_lookup = "item__company"
    action = None

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["action"] = self.action
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = self.action
        return context


class InventoryPickView(InventoryAdjustBaseView):
    permission_required = "can_pick_item"
    permission_match_any = False
    action = "pick"

    def get_page_title(self):
        return f"Pick Item: {self.object.item.name}"

    @transaction.atomic
    def form_valid(self, form):
        picked_qty = form.cleaned_data["quantity"]
        self.object.quantity -= picked_qty
        self.object.updated_by = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class InventoryStoreView(InventoryAdjustBaseView):
    permission_required = "can_store_item"
    permission_match_any = False
    action = "store"

    def get_page_title(self):
        return f"Store Item: {self.object.item.name}"

    @transaction.atomic
    def form_valid(self, form):
        stored_qty = form.cleaned_data["quantity"]
        self.object.quantity += stored_qty
        self.object.updated_by = self.request.user
        self.object.save()
        return redirect(self.get_success_url())


class InventoryStoreNewView(
    ProfilePermissionMixin, CompanyMixin, PageTitleMixin, FormView
):
    """Stores an item into a selected location (new record or adds to existing)."""

    permission_required = "can_store_item"
    form_class = StoreNewInventoryForm
    page_title = "Store Item in Location"
    template_name = "inventory/manage_inventory/inventory_store_new_form.html"
    success_url = reverse_lazy("inventory_list")

    @transaction.atomic
    def form_valid(self, form):
        item = form.cleaned_data["item"]
        location = form.cleaned_data["location"]
        quantity = form.cleaned_data["quantity"]

        inventory_level, _ = InventoryLevel.objects.get_or_create(
            item=item,
            location=location,
            defaults={"quantity": 0},
        )
        inventory_level.quantity += quantity
        inventory_level.updated_by = self.request.user
        inventory_level.save()

        return super().form_valid(form)
