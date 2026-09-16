from django.contrib import admin

from .models import Sale, SaleItem


class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 1
    readonly_fields = (
        "line_total",
        "line_cost",
        "line_profit",
    )


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "business",
        "sale_date",
        "subtotal",
        "discount_amount",
        "total_amount",
        "gross_profit",
        "payment_method",
        "status",
        "created_by",
    )

    search_fields = (
        "invoice_number",
        "business__name",
        "created_by__email",
    )

    list_filter = (
        "business",
        "payment_method",
        "status",
        "sale_date",
    )

    readonly_fields = (
        "subtotal",
        "total_cost",
        "total_amount",
        "gross_profit",
        "created_at",
    )

    inlines = [SaleItemInline]
