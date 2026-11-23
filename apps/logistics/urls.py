from django.urls import path

from apps.logistics.views import (
    ImportDemoOrdersView,
    OrderItemListView,
    OrderItemPickView,
    OrderListView,
)

urlpatterns = [
    path(
        "orders/import/", ImportDemoOrdersView.as_view(), name="order_import"
    ),
    path("orders/", OrderListView.as_view(), name="order_list"),
    path(
        "orders/<int:order_pk>/pick/",
        OrderItemListView.as_view(),
        name="order_item_list",
    ),
    path(
        "orders/<int:order_pk>/pick/<int:pk>/",
        OrderItemPickView.as_view(),
        name="order_item_pick",
    ),
]
