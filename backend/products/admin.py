from django.contrib import admin

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "business",
        "created_at",
    )
    search_fields = (
        "name",
        "business__name",
    )
    list_filter = (
        "business",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "business",
        "category",
        "unit",
        "buying_price",
        "selling_price",
        "stock_quantity",
        "reorder_level",
        "is_active",
    )

    search_fields = (
        "name",
        "sku",
        "business__name",
    )

    list_filter = (
        "business",
        "category",
        "unit",
        "is_active",
    )
