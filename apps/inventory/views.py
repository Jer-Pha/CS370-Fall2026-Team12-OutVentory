from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from apps.core.mixins import PageTitleMixin
from apps.inventory.forms import BuildingForm
from apps.inventory.mixins import CompanyQuerySetMixin, OwnerRequiredMixin
from apps.inventory.models import Building


class BuildingCreateView(OwnerRequiredMixin, PageTitleMixin, CreateView):
    model = Building
    form_class = BuildingForm
    template_name = "inventory/buildings/building_form.html"
    success_url = reverse_lazy("building_list")
    page_title = "Add Building"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["company"] = self.request.user.profile.company
        return kwargs


class BuildingListView(
    OwnerRequiredMixin, CompanyQuerySetMixin, PageTitleMixin, ListView
):
    model = Building
    template_name = "inventory/buildings/building_list.html"
    context_object_name = "buildings"
    paginate_by = 20
    page_title = "Buildings"


class BuildingUpdateView(
    OwnerRequiredMixin, CompanyQuerySetMixin, PageTitleMixin, UpdateView
):
    model = Building
    form_class = BuildingForm
    template_name = "inventory/buildings/building_form.html"
    success_url = reverse_lazy("building_list")

    def get_page_title(self):
        return f"Edit Building: {self.object.name}"


class BuildingDeleteView(
    OwnerRequiredMixin,
    CompanyQuerySetMixin,
    PageTitleMixin,
    DeleteView,
):
    model = Building
    template_name = "inventory/buildings/building_confirm_delete.html"
    success_url = reverse_lazy("building_list")

    def get_page_title(self):
        return f"Delete Building: {self.object.name}"
