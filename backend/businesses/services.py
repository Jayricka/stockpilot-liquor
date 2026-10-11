from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework.exceptions import ValidationError

from billing.models import Subscription
from billing.services.entitlements import EntitlementService
from billing.services.subscriptions import SubscriptionService
from products.services import ProductService

from .models import Business, BusinessMembership


class BusinessService:
    @staticmethod
    @transaction.atomic
    def create_business(user, validated_data):
        name = validated_data["name"].strip()

        if Business.objects.filter(
            name__iexact=name,
            memberships__user=user,
            memberships__is_active=True,
        ).exists():
            raise ValueError(
                "You already have a business with this name."
            )

        validated_data["name"] = name
        business = Business.objects.create(**validated_data)
        BusinessMembership.objects.create(
            user=user,
            business=business,
            role=BusinessMembership.Role.OWNER,
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
        ProductService.create_default_categories(business)
        subscription = SubscriptionService.create_trial(
            business=business,
            plan=plan,
        )
        return business, subscription


class BusinessMembershipService:
    MEMBER_ROLES = {
        BusinessMembership.Role.MANAGER,
        BusinessMembership.Role.STAFF,
    }

    @staticmethod
    def _get_business(business_id):
        business = Business.objects.select_for_update().filter(
            pk=business_id,
            is_active=True,
        ).first()
        if business is None:
            raise ValidationError("Business not found or inactive.")

        subscription = (
            Subscription.objects.select_for_update()
            .filter(business=business)
            .first()
        )
        if subscription is None:
            raise ValidationError("Business subscription not found.")

        SubscriptionService.expire_trial(subscription)
        subscription.refresh_from_db(fields=["status"])

        if subscription.status not in {
            Subscription.Status.TRIALING,
            Subscription.Status.ACTIVE,
        }:
            raise ValidationError(
                "An active subscription or trial is required "
                "to manage team members."
            )
        return business

    @staticmethod
    def _get_actor_membership(business, actor):
        membership = BusinessMembership.objects.filter(
            business=business,
            user=actor,
            is_active=True,
        ).first()
        if membership is None:
            raise ValidationError(
                "You are not an active member of this business."
            )
        return membership

    @staticmethod
    def _get_limit(business, feature):
        limit = EntitlementService.get_limit(business, feature)
        if limit is None:
            raise ValidationError(
                f"The plan has no valid '{feature}' limit."
            )
        return limit

    @classmethod
    def _check_capacity(cls, business, role, membership=None):
        active = BusinessMembership.objects.filter(
            business=business,
            is_active=True,
        )

        if membership is None or not membership.is_active:
            limit = cls._get_limit(business, "max_users")
            if active.count() >= limit:
                raise ValidationError(
                    f"Your plan allows at most {limit} active users."
                )

        if membership and membership.is_active:
            if membership.role == role:
                return

        limit_feature = {
            BusinessMembership.Role.MANAGER: "max_managers",
            BusinessMembership.Role.STAFF: "max_staff",
        }[role]
        limit = cls._get_limit(business, limit_feature)
        if active.filter(role=role).count() >= limit:
            raise ValidationError(
                f"Your plan allows at most {limit} "
                f"{role.lower()} members."
            )

    @classmethod
    @transaction.atomic
    def add_member(cls, *, business_id, actor, email, role):
        business = cls._get_business(business_id)
        actor_membership = cls._get_actor_membership(
            business,
            actor,
        )
        role = role.upper()

        if role not in cls.MEMBER_ROLES:
            raise ValidationError("Role must be MANAGER or STAFF.")

        if actor_membership.role == BusinessMembership.Role.MANAGER:
            if role != BusinessMembership.Role.STAFF:
                raise ValidationError(
                    "Managers can add staff members only."
                )
        elif actor_membership.role != BusinessMembership.Role.OWNER:
            raise ValidationError(
                "Only owners and managers can add team members."
            )

        User = get_user_model()
        user = User.objects.filter(
            email__iexact=email.strip(),
            is_active=True,
        ).first()
        if user is None:
            raise ValidationError(
                "No active user account exists for this email."
            )

        membership = BusinessMembership.objects.filter(
            business=business,
            user=user,
        ).first()

        if membership and membership.is_active:
            raise ValidationError(
                "This user is already an active member."
            )

        cls._check_capacity(business, role, membership)

        if membership:
            membership.role = role
            membership.is_active = True
            membership.save(update_fields=["role", "is_active"])
            return membership

        return BusinessMembership.objects.create(
            business=business,
            user=user,
            role=role,
            is_active=True,
        )

    @classmethod
    @transaction.atomic
    def update_member_role(
        cls, *, business_id, actor, user_id, role
    ):
        business = cls._get_business(business_id)
        actor_membership = cls._get_actor_membership(
            business,
            actor,
        )
        target = BusinessMembership.objects.select_for_update().filter(
            business=business,
            user_id=user_id,
            is_active=True,
        ).first()

        if target is None:
            raise ValidationError("Active team member not found.")
        if target.role == BusinessMembership.Role.OWNER:
            raise ValidationError("The owner role cannot be changed.")

        role = role.upper()
        if role not in cls.MEMBER_ROLES:
            raise ValidationError("Role must be MANAGER or STAFF.")

        if actor_membership.role == BusinessMembership.Role.MANAGER:
            if (
                target.role != BusinessMembership.Role.STAFF
                or role != BusinessMembership.Role.STAFF
            ):
                raise ValidationError(
                    "Managers can manage staff only."
                )
        elif actor_membership.role != BusinessMembership.Role.OWNER:
            raise ValidationError(
                "Only owners and managers can manage members."
            )

        cls._check_capacity(business, role, target)
        target.role = role
        target.save(update_fields=["role"])
        return target

    @classmethod
    @transaction.atomic
    def deactivate_member(cls, *, business_id, actor, user_id):
        business = cls._get_business(business_id)
        actor_membership = cls._get_actor_membership(
            business,
            actor,
        )
        target = BusinessMembership.objects.select_for_update().filter(
            business=business,
            user_id=user_id,
            is_active=True,
        ).first()

        if target is None:
            raise ValidationError("Active team member not found.")
        if target.role == BusinessMembership.Role.OWNER:
            raise ValidationError("The owner cannot be deactivated.")
        if target.user_id == actor.id:
            raise ValidationError(
                "You cannot deactivate your own membership."
            )

        if actor_membership.role == BusinessMembership.Role.MANAGER:
            if target.role != BusinessMembership.Role.STAFF:
                raise ValidationError(
                    "Managers can deactivate staff only."
                )
        elif actor_membership.role != BusinessMembership.Role.OWNER:
            raise ValidationError(
                "Only owners and managers can deactivate members."
            )

        target.is_active = False
        target.save(update_fields=["is_active"])
