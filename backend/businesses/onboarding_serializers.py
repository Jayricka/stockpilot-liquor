from rest_framework import serializers

from billing.models import Plan

from .models import Business
from .services import BusinessOnboardingService


class BusinessOnboardingSerializer(
    serializers.ModelSerializer
):
    plan = serializers.SlugRelatedField(
        slug_field="code",
        queryset=Plan.objects.filter(
            is_active=True,
        ),
    )

    class Meta:
        model = Business
        fields = [
            "name",
            "business_type",
            "phone",
            "email",
            "address",
            "license_number",
            "plan",
        ]

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Business name is required."
            )

        return value

    def validate_phone(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Business phone number is required."
            )

        return value

    def create(self, validated_data):
        user = self.context["request"].user

        try:
            business, subscription = (
                BusinessOnboardingService.onboard(
                    user=user,
                    validated_data=validated_data,
                )
            )
        except ValueError as exc:
            raise serializers.ValidationError(
                {"name": str(exc)}
            ) from exc

        self.subscription = subscription

        return business
