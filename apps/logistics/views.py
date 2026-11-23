from random import randint

from django.contrib import messages
from django.db import transaction
from django.db.models import Count, F, Prefetch, Sum
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, UpdateView

from apps.companies.mixins import CompanyMixin
from apps.core.mixins import PageTitleMixin
from apps.inventory.models import InventoryLevel
from apps.logistics.forms import OrderItemPickForm
from apps.logistics.models import Order, OrderItem
from apps.logistics.utils import generate_demo_orders_for_company
from apps.users.mixins import ProfilePermissionMixin


class OrderListView(
    ProfilePermissionMixin, CompanyMixin, PageTitleMixin, ListView
):
    permission_required = "can_pick_order"
    model = Order
    context_object_name = "orders"
    paginate_by = 20
    page_title = "Orders"
    template_name = "logistics/orders/order_list.html"

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .annotate(
                item_count=Count("order_items", distinct=True),
                total_quantity=Sum("order_items__quantity_total"),
            )
            .order_by("-created_at", "-updated_at")
        )


class OrderItemBaseView(ProfilePermissionMixin, CompanyMixin, PageTitleMixin):
    permission_required = "can_pick_order"
    model = OrderItem
    company_lookup = "order__company"

    def get_queryset(self):
        order_pk = self.kwargs.get("order_pk")
        self.order = get_object_or_404(Order, pk=order_pk)
        return (
            super()
            .get_queryset()
            .filter(order=self.order)
            .select_related(
                "item",
                "updated_by__profile",
                "order__company",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["order"] = self.order
        return context


class OrderItemListView(OrderItemBaseView, ListView):
    context_object_name = "order_items"
    page_title = "Orders"
    template_name = "logistics/orders/order_item_list.html"

    def get_page_title(self):
        return f"Order {self.order.order_number}"


class OrderItemPickView(OrderItemBaseView, UpdateView):
    form_class = OrderItemPickForm
    template_name = "logistics/orders/order_item_pick.html"
    success_url = reverse_lazy("order_list")

    def get_page_title(self):
        return f"Pick Item: {self.object.item.name}"

    def get_queryset(self):
        super_qs = super().get_queryset()
        self.success_url = reverse_lazy(
            "order_item_list", kwargs={"order_pk": self.order.pk}
        )
        item_inventory_prefetch = Prefetch(
            "item__inventory_levels",
            queryset=InventoryLevel.objects.filter(
                quantity__gte=1
            ).select_related("location__building"),
            to_attr="available_inventory",
        )
        return super_qs.prefetch_related(item_inventory_prefetch)

    @transaction.atomic
    def form_valid(self, form):
        picked_qty = form.cleaned_data["quantity"]
        self.object.quantity_picked += picked_qty
        self.object.updated_by = self.request.user
        self.object.save()

        InventoryLevel.objects.filter(pk=form.inventory_instance.pk).update(
            quantity=F("quantity") - picked_qty
        )

        self.order.update_status()

        return redirect(self.get_success_url())


class ImportDemoOrdersView(ProfilePermissionMixin, CompanyMixin, View):
    permission_required = "can_pick_order"

    def post(self, request, *args, **kwargs):
        company = getattr(self, "company", None) or getattr(
            request, "company", None
        )
        if not company and hasattr(self, "get_company"):
            company = self.get_company()

        if company:
            created_count = generate_demo_orders_for_company(
                company, count=randint(2, 10)
            )
            if created_count > 0:
                messages.success(
                    request,
                    f"Successfully imported {created_count} order(s).",
                )
            else:
                messages.warning(
                    request,
                    "Could not import orders. Make sure items have available inventory (quantity >= 1).",
                )
        else:
            messages.error(
                request, "Could not determine the active company context."
            )

        return redirect("order_list")
