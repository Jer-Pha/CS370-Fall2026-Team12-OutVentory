from django.urls import path

from apps.inventory.views import (
    BuildingCreateView,
    BuildingDeleteView,
    BuildingListView,
    BuildingUpdateView,
    ItemCreateView,
    ItemDeleteView,
    ItemListView,
    ItemUpdateView,
    LocationCreateView,
    LocationDeleteView,
    LocationListView,
    LocationUpdateView,
)

# Building URLs
urlpatterns = [
    path("buildings/", BuildingListView.as_view(), name="building_list"),
    path(
        "buildings/add/", BuildingCreateView.as_view(), name="building_create"
    ),
    path(
        "buildings/<int:pk>/edit/",
        BuildingUpdateView.as_view(),
        name="building_update",
    ),
    path(
        "<int:pk>/delete/",
        BuildingDeleteView.as_view(),
        name="building_delete",
    ),
]

# Item URLs
urlpatterns += [
    path("items/", ItemListView.as_view(), name="item_list"),
    path("items/add/", ItemCreateView.as_view(), name="item_create"),
    path("items/<int:pk>/edit/", ItemUpdateView.as_view(), name="item_update"),
    path(
        "items/<int:pk>/delete/",
        ItemDeleteView.as_view(),
        name="item_delete",
    ),
]

# Location URLs
urlpatterns += [
    path("locations/", LocationListView.as_view(), name="location_list"),
    path(
        "locations/add/", LocationCreateView.as_view(), name="location_create"
    ),
    path(
        "locations/<int:pk>/edit/",
        LocationUpdateView.as_view(),
        name="location_update",
    ),
    path(
        "locations/<int:pk>/delete/",
        LocationDeleteView.as_view(),
        name="location_delete",
    ),
]
