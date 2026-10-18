from django.contrib import admin

from apps.inventory.models import (
    Building,
    InventoryLevel,
    Item,
    StorageLocation,
)

admin.site.register(Building)
admin.site.register(StorageLocation)
admin.site.register(Item)
admin.site.register(InventoryLevel)
