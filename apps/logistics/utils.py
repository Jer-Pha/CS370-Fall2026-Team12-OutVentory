import random

from django.db.models import F, Sum

from apps.inventory.models import Item
from apps.logistics.models import Order, OrderItem


def generate_demo_orders_for_company(company, count=5):
    """
    Generates demo orders for a given company based on current inventory
    and unpicked quantities.
    """
    items = Item.objects.filter(company=company).prefetch_related(
        "inventory_levels", "order_items"
    )
    if not items.exists():
        return 0

    script_allocations = {}
    item_availability = {}

    for item in items:
        # 1. Total inventory across all locations
        total_inv = (
            item.inventory_levels.aggregate(total=Sum("quantity"))["total"]
            or 0
        )

        # 2. Total unpicked quantities in existing orders
        unpicked_orders = (
            item.order_items.filter(quantity_picked__lt=F("quantity_total"))
            .annotate(remaining=F("quantity_total") - F("quantity_picked"))
            .aggregate(total=Sum("remaining"))["total"]
            or 0
        )

        available = total_inv - unpicked_orders
        if available > 0:
            item_availability[item] = available

    if not item_availability:
        return 0

    eligible_items = list(item_availability.keys())
    orders_created = 0

    for _ in range(count):
        num_items_to_pick = random.randint(1, min(4, len(eligible_items)))
        chosen_items = random.sample(eligible_items, num_items_to_pick)

        order_items_to_create = []
        for item in chosen_items:
            net_available = item_availability[item] - script_allocations.get(
                item, 0
            )
            if net_available <= 0:
                continue

            max_possible_qty = min(net_available, 10)
            chosen_qty = random.randint(1, max_possible_qty)
            script_allocations[item] = (
                script_allocations.get(item, 0) + chosen_qty
            )

            order_items_to_create.append(
                OrderItem(
                    item=item,
                    quantity_total=chosen_qty,
                    quantity_picked=0,
                )
            )

        if order_items_to_create:
            order = Order.objects.create(company=company)
            for order_item in order_items_to_create:
                order_item.order = order
            OrderItem.objects.bulk_create(order_items_to_create)
            orders_created += 1

    return orders_created
