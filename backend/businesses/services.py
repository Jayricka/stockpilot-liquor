import hashlib
import secrets
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from billing.models import Subscription
from billing.services.entitlements import EntitlementService
from billing.services.subscriptions import SubscriptionService
from products.services import ProductService

from .models import (
    Business,
    BusinessInvitation,
    BusinessMembership,
)


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



class BusinessInvitationService:
    INVITATION_VALIDITY_DAYS = 7

    @classmethod
    @transaction.atomic
    def create_invitation(
        cls,
        *,
        business_id,
        actor,
        email,
        role,
    ):
        business = BusinessMembershipService._get_business(
            business_id
        )
        actor_membership = (
            BusinessMembershipService._get_actor_membership(
                business,
                actor,
            )
        )

        email = str(email).strip().lower()
        role = str(role).upper()

        if role not in BusinessMembershipService.MEMBER_ROLES:
            raise ValidationError(
                "Role must be MANAGER or STAFF."
            )

        if actor_membership.role == BusinessMembership.Role.MANAGER:
            if role != BusinessMembership.Role.STAFF:
                raise ValidationError(
                    "Managers can invite staff members only."
                )
        elif actor_membership.role != BusinessMembership.Role.OWNER:
            raise ValidationError(
                "Only owners and managers can invite members."
            )

        User = get_user_model()
        user = User.objects.filter(
            email__iexact=email,
            is_active=True,
        ).first()

        if user and BusinessMembership.objects.filter(
            business=business,
            user=user,
            is_active=True,
        ).exists():
            raise ValidationError(
                "This user is already an active member."
            )

        now = timezone.now()

        BusinessInvitation.objects.filter(
            business=business,
            status=BusinessInvitation.Status.PENDING,
            expires_at__lte=now,
        ).update(
            status=BusinessInvitation.Status.EXPIRED,
        )

        if BusinessInvitation.objects.filter(
            business=business,
            email=email,
            status=BusinessInvitation.Status.PENDING,
        ).exists():
            raise ValidationError(
                "A pending invitation already exists for this email."
            )

        active_memberships = BusinessMembership.objects.filter(
            business=business,
            is_active=True,
        )
        pending = BusinessInvitation.objects.filter(
            business=business,
            status=BusinessInvitation.Status.PENDING,
            expires_at__gt=now,
        )

        user_limit = BusinessMembershipService._get_limit(
            business,
            "max_users",
        )
        pending_user_count = pending.count()

        if (
            active_memberships.count()
            + pending_user_count
            >= user_limit
        ):
            raise ValidationError(
                f"Your plan allows at most {user_limit} "
                "active users and pending invitations combined."
            )

        role_feature = {
            BusinessMembership.Role.MANAGER: "max_managers",
            BusinessMembership.Role.STAFF: "max_staff",
        }[role]
        role_limit = BusinessMembershipService._get_limit(
            business,
            role_feature,
        )
        active_role_count = active_memberships.filter(
            role=role,
        ).count()
        pending_role_count = pending.filter(role=role).count()

        if (
            active_role_count + pending_role_count
            >= role_limit
        ):
            raise ValidationError(
                f"Your plan allows at most {role_limit} "
                f"{role.lower()} members and invitations combined."
            )

        raw_token = secrets.token_urlsafe(32)
        token_hash = hashlib.sha256(
            raw_token.encode("utf-8")
        ).hexdigest()

        invitation = BusinessInvitation.objects.create(
            business=business,
            email=email,
            role=role,
            token_hash=token_hash,
            invited_by=actor,
            expires_at=now + timedelta(
                days=cls.INVITATION_VALIDITY_DAYS
            ),
        )

        return invitation, raw_token

    @classmethod
    @transaction.atomic
    def revoke_invitation(
        cls,
        *,
        business_id,
        actor,
        invitation_id,
    ):
        business = BusinessMembershipService._get_business(
            business_id
        )
        actor_membership = (
            BusinessMembershipService._get_actor_membership(
                business,
                actor,
            )
        )
        invitation = (
            BusinessInvitation.objects.select_for_update()
            .filter(
                business=business,
                pk=invitation_id,
                status=BusinessInvitation.Status.PENDING,
            )
            .first()
        )

        if invitation is None:
            raise ValidationError(
                "Pending invitation not found."
            )

        if invitation.expires_at <= timezone.now():
            invitation.status = BusinessInvitation.Status.EXPIRED
            invitation.save(
                update_fields=["status", "updated_at"],
            )
            return invitation

        if actor_membership.role == BusinessMembership.Role.MANAGER:
            if invitation.role != BusinessInvitation.Role.STAFF:
                raise ValidationError(
                    "Managers can revoke staff invitations only."
                )
        elif actor_membership.role != BusinessMembership.Role.OWNER:
            raise ValidationError(
                "Only owners and managers can revoke invitations."
            )

        invitation.status = BusinessInvitation.Status.REVOKED
        invitation.save(
            update_fields=["status", "updated_at"],
        )
        return invitation

    @classmethod
    def accept_invitation(cls, *, token, actor):
        if not token or not getattr(actor, "is_authenticated", False):
            raise ValidationError(
                "A valid invitation token and authenticated user "
                "are required."
            )

        if not actor.is_active:
            raise ValidationError("This user account is inactive.")

        token_hash = hashlib.sha256(
            token.encode("utf-8")
        ).hexdigest()

        # Resolve the business first so lock order matches the other
        # invitation operations: business, then invitation.
        invitation_ref = BusinessInvitation.objects.filter(
            token_hash=token_hash,
        ).values("pk", "business_id").first()

        if invitation_ref is None:
            raise ValidationError("Invalid invitation token.")

        expired = False
        membership = None

        with transaction.atomic():
            business = BusinessMembershipService._get_business(
                invitation_ref["business_id"]
            )

            invitation = (
                BusinessInvitation.objects.select_for_update()
                .filter(
                    pk=invitation_ref["pk"],
                    token_hash=token_hash,
                    business=business,
                )
                .first()
            )

            if (
                invitation is None
                or invitation.status
                != BusinessInvitation.Status.PENDING
            ):
                raise ValidationError(
                    "This invitation is no longer available."
                )

            now = timezone.now()

            if invitation.expires_at <= now:
                invitation.status = BusinessInvitation.Status.EXPIRED
                invitation.save(
                    update_fields=["status", "updated_at"],
                )
                expired = True
            else:
                if actor.email.strip().lower() != invitation.email:
                    raise ValidationError(
                        "This invitation belongs to a different email."
                    )

                existing = (
                    BusinessMembership.objects.select_for_update()
                    .filter(
                        business=business,
                        user=actor,
                    )
                    .first()
                )

                if existing and existing.is_active:
                    raise ValidationError(
                        "You are already an active member."
                    )

                BusinessMembershipService._check_capacity(
                    business,
                    invitation.role,
                    existing,
                )

                if existing:
                    existing.role = invitation.role
                    existing.is_active = True
                    existing.save(
                        update_fields=["role", "is_active"],
                    )
                    membership = existing
                else:
                    membership = BusinessMembership.objects.create(
                        business=business,
                        user=actor,
                        role=invitation.role,
                        is_active=True,
                    )

                invitation.status = BusinessInvitation.Status.ACCEPTED
                invitation.accepted_by = actor
                invitation.accepted_at = now
                invitation.save(
                    update_fields=[
                        "status",
                        "accepted_by",
                        "accepted_at",
                        "updated_at",
                    ],
                )

        # Raise outside the transaction so the EXPIRED status commits.
        if expired:
            raise ValidationError("This invitation has expired.")

        return membership
