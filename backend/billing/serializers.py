from rest_framework import serializers

from .models import Payment, Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):

    class Meta:
        model = Plan
        fields = [
            "code",
            "name",
            "price",
            "currency",
            "trial_days",
        ]


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "currency",
            "phone_number",
            "status",
            "mpesa_receipt",
            "created_at",
            "completed_at",
        ]


class SubscriptionSerializer(
    serializers.ModelSerializer
):
    plan = PlanSerializer(read_only=True)
    trial_active = serializers.BooleanField(
        source="is_trial_active",
        read_only=True,
    )
    trial_days_remaining = serializers.IntegerField(
        read_only=True,
    )

    class Meta:
        model = Subscription
        fields = [
            "id",
            "plan",
            "status",
            "trial_started_at",
            "trial_ends_at",
            "trial_active",
            "trial_days_remaining",
            "current_period_start",
            "current_period_end",
            "cancelled_at",
            "created_at",
            "updated_at",
        ]
