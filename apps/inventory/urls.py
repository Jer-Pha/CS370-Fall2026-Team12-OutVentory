from django.urls import path

from apps.inventory.views import (
    BuildingCreateView,
    BuildingDeleteView,
    BuildingListView,
    BuildingUpdateView,
)

urlpatterns = [
    path("buildings/", BuildingListView.as_view(), name="building_list"),
    path(
        "buildings/add/", BuildingCreateView.as_view(), name="building_create"
    ),
    path(
        "<int:pk>/edit/", BuildingUpdateView.as_view(), name="building_update"
    ),
    path(
        "<int:pk>/delete/",
        BuildingDeleteView.as_view(),
        name="building_delete",
    ),
]
