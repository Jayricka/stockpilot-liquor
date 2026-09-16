from django.contrib import admin

from .models import Supplier


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "business",
        "phone",
        "email",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "phone",
        "email",
        "business__name",
    )

    list_filter = (
        "business",
        "is_active",
    )
