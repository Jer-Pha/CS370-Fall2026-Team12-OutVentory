from django.contrib import admin

from apps.logistics.models import Order, OrderItem, Shipment, ShipmentItem

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Shipment)
admin.site.register(ShipmentItem)
