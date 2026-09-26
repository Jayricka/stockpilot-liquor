from django.db import transaction

from billing.services.subscriptions import (
    SubscriptionService,
)
from products.services import ProductService

from .models import Business, BusinessMembership


class BusinessService:

    @staticmethod
    @transaction.atomic
    def create_business(user, validated_data):
        business_name = validated_data["name"].strip()

        existing_business = (
            Business.objects
            .filter(
                name__iexact=business_name,
                memberships__user=user,
                memberships__is_active=True,
            )
            .first()
        )

        if existing_business:
            raise ValueError(
                "You already have a business with this name."
            )

        validated_data["name"] = business_name

        business = Business.objects.create(
            **validated_data
        )

        BusinessMembership.objects.create(
            user=user,
            business=business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        return business


class BusinessOnboardingService:

    @staticmethod
    @transaction.atomic
    def onboard(user, validated_data):
        plan = validated_data.pop("plan")

        business = BusinessService.create_business(
            user=user,
            validated_data=validated_data,
        )

        ProductService.create_default_categories(
            business
        )

        subscription = SubscriptionService.create_trial(
            business=business,
            plan=plan,
        )

        return business, subscription
