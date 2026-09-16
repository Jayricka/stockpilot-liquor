from django.contrib import admin

from .models import DeliveryOrder


@admin.register(DeliveryOrder)
class DeliveryOrderAdmin(admin.ModelAdmin):
    list_display = [
        "customer_name",
        "customer_phone",
        "sale",
        "business",
        "status",
        "assigned_to",
        "delivery_fee",
        "created_at",
    ]

    list_filter = [
        "status",
        "business",
        "created_at",
    ]

    search_fields = [
        "customer_name",
        "customer_phone",
        "sale__invoice_number",
    ]

    readonly_fields = [
        "assigned_at",
        "delivered_at",
        "created_at",
        "updated_at",
    ]
