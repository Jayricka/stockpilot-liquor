from django.contrib import admin

from .models import Business, BusinessMembership


@admin.register(Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "business_type",
        "phone",
        "is_active",
        "created_at",
    )
    search_fields = (
        "name",
        "phone",
        "email",
        "license_number",
    )
    list_filter = (
        "business_type",
        "is_active",
    )


@admin.register(BusinessMembership)
class BusinessMembershipAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "business",
        "role",
        "is_active",
        "created_at",
    )
    list_filter = (
        "role",
        "is_active",
    )
    search_fields = (
        "user__email",
        "business__name",
    )
