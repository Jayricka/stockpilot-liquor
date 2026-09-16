from django.contrib import admin

from .models import Purchase, PurchaseItem, StockMovement


class PurchaseItemInline(admin.TabularInline):
    model = PurchaseItem
    extra = 1
    readonly_fields = ("line_total",)


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "reference_number",
        "business",
        "supplier",
        "purchase_date",
        "total_amount",
        "status",
        "created_by",
    )

    search_fields = (
        "reference_number",
        "supplier__name",
        "business__name",
    )

    list_filter = (
        "business",
        "supplier",
        "status",
        "purchase_date",
    )

    readonly_fields = (
        "total_amount",
        "created_at",
        "updated_at",
    )

    inlines = [PurchaseItemInline]


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "business",
        "movement_type",
        "quantity",
        "balance_after",
        "performed_by",
        "created_at",
    )

    search_fields = (
        "product__name",
        "business__name",
        "performed_by__email",
    )

    list_filter = (
        "business",
        "movement_type",
        "created_at",
    )

    readonly_fields = (
        "created_at",
    )
