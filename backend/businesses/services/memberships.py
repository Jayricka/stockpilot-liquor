from django.contrib.auth import get_user_model
from django.db import transaction

from billing.models import Subscription
from billing.services.entitlements import (
    PlanEntitlementService,
)
from billing.services.subscriptions import (
    SubscriptionService,
)

from ..models import BusinessMembership


User = get_user_model()


class BusinessMembershipService:

    @staticmethod
    def get_subscription(business):
        try:
            subscription = (
                Subscription.objects
                .select_related("plan")
                .get(business=business)
            )
        except Subscription.DoesNotExist:
            raise ValueError(
                "This business does not have a subscription."
            )

        SubscriptionService.expire_trial(subscription)

        if subscription.status not in {
            Subscription.Status.TRIALING,
            Subscription.Status.ACTIVE,
        }:
            raise ValueError(
                "This subscription is not active."
            )

        return subscription

    @staticmethod
    def get_active_memberships(business):
        return BusinessMembership.objects.filter(
            business=business,
            is_active=True,
        )

    @classmethod
    def validate_user_limit(cls, business, plan):
        limit = PlanEntitlementService.get_limit(
            plan,
            "max_users",
        )

        current_count = cls.get_active_memberships(
            business
        ).count()

        if limit is not None and current_count >= limit:
            raise ValueError(
                f"The {plan.name} plan allows "
                f"up to {limit} active user(s)."
            )

    @classmethod
    def validate_role_limit(
        cls,
        business,
        plan,
        role,
    ):
        role_limits = {
            BusinessMembership.Role.OWNER: "max_owners",
            BusinessMembership.Role.MANAGER: "max_managers",
            BusinessMembership.Role.STAFF: "max_staff",
        }

        feature = role_limits[role]

        limit = PlanEntitlementService.get_limit(
            plan,
            feature,
        )

        current_count = (
            cls.get_active_memberships(business)
            .filter(role=role)
            .count()
        )

        if limit is not None and current_count >= limit:
            raise ValueError(
                f"The {plan.name} plan allows "
                f"up to {limit} {role.lower()} member(s)."
            )

    @classmethod
    @transaction.atomic
    def add_member(
        cls,
        business,
        email,
        role,
    ):
        subscription = cls.get_subscription(
            business
        )

        if role not in BusinessMembership.Role.values:
            raise ValueError(
                "Invalid business membership role."
            )

        normalized_email = email.strip().lower()

        try:
            user = User.objects.get(
                email__iexact=normalized_email,
            )
        except User.DoesNotExist:
            raise ValueError(
                "No registered user exists with this email."
            )

        membership = (
            BusinessMembership.objects
            .select_for_update()
            .filter(
                user=user,
                business=business,
            )
            .first()
        )

        if membership and membership.is_active:
            raise ValueError(
                "This user is already an active member."
            )

        cls.validate_user_limit(
            business,
            subscription.plan,
        )

        cls.validate_role_limit(
            business,
            subscription.plan,
            role,
        )

        if membership:
            membership.role = role
            membership.is_active = True
            membership.save(
                update_fields=[
                    "role",
                    "is_active",
                ],
            )
            return membership

        return BusinessMembership.objects.create(
            user=user,
            business=business,
            role=role,
            is_active=True,
        )

    @staticmethod
    @transaction.atomic
    def deactivate_member(
        business,
        user_id,
    ):
        try:
            membership = (
                BusinessMembership.objects
                .select_for_update()
                .get(
                    business=business,
                    user_id=user_id,
                    is_active=True,
                )
            )
        except BusinessMembership.DoesNotExist:
            raise ValueError(
                "Active membership was not found."
            )

        if membership.role == (
            BusinessMembership.Role.OWNER
        ):
            raise ValueError(
                "The business owner cannot be removed."
            )

        membership.is_active = False
        membership.save(
            update_fields=["is_active"],
        )

        return membership

    @classmethod
    @transaction.atomic
    def change_role(
        cls,
        business,
        user_id,
        role,
    ):
        subscription = cls.get_subscription(
            business
        )

        if role not in BusinessMembership.Role.values:
            raise ValueError(
                "Invalid business membership role."
            )

        try:
            membership = (
                BusinessMembership.objects
                .select_for_update()
                .get(
                    business=business,
                    user_id=user_id,
                    is_active=True,
                )
            )
        except BusinessMembership.DoesNotExist:
            raise ValueError(
                "Active membership was not found."
            )

        if membership.role == role:
            return membership

        if membership.role == (
            BusinessMembership.Role.OWNER
        ):
            raise ValueError(
                "The business owner role cannot be changed."
            )

        cls.validate_role_limit(
            business,
            subscription.plan,
            role,
        )

        membership.role = role
        membership.save(
            update_fields=["role"],
        )

        return membership
