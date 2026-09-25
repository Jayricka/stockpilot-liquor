from django.contrib import admin

from .models import Payment, Plan, Subscription


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "code",
        "price",
        "currency",
        "trial_days",
        "is_active",
    )

    list_filter = (
        "is_active",
    )


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "business",
        "plan",
        "status",
        "trial_ends_at",
        "current_period_end",
    )

    list_filter = (
        "status",
        "plan",
    )

    search_fields = (
        "business__name",
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "subscription",
        "amount",
        "currency",
        "status",
        "phone_number",
        "mpesa_receipt",
        "created_at",
    )

    list_filter = (
        "status",
        "currency",
    )

    search_fields = (
        "phone_number",
        "mpesa_receipt",
        "checkout_request_id",
    )

    readonly_fields = (
        "created_at",
        "completed_at",
    )
