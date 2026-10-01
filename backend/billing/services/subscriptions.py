from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from ..models import Plan, Subscription


class SubscriptionService:

    @staticmethod
    @transaction.atomic
    def create_trial(business, plan):
        if Subscription.objects.filter(
            business=business
        ).exists():
            raise ValueError(
                "This business already has a subscription."
            )

        now = timezone.now()

        subscription = Subscription.objects.create(
            business=business,
            plan=plan,
            status=Subscription.Status.TRIALING,
            trial_started_at=now,
            trial_ends_at=now + timedelta(
                days=plan.trial_days
            ),
        )

        return subscription

    @staticmethod
    @transaction.atomic
    def activate(subscription):
        allowed_statuses = {
            Subscription.Status.TRIALING,
            Subscription.Status.PAST_DUE,
        }

        if subscription.status not in allowed_statuses:
            raise ValueError(
                "Only trialing or past due subscriptions "
                "can be activated."
            )

        subscription.status = Subscription.Status.ACTIVE
        subscription.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return subscription

    @staticmethod
    @transaction.atomic
    def mark_past_due(subscription):
        if subscription.status != Subscription.Status.ACTIVE:
            raise ValueError(
                "Only active subscriptions can be marked "
                "past due."
            )

        subscription.status = Subscription.Status.PAST_DUE
        subscription.save(
            update_fields=[
                "status",
                "updated_at",
            ]
        )

        return subscription

    @staticmethod
    @transaction.atomic
    def cancel(subscription):
        allowed_statuses = {
            Subscription.Status.TRIALING,
            Subscription.Status.ACTIVE,
            Subscription.Status.PAST_DUE,
        }

        if subscription.status not in allowed_statuses:
            raise ValueError(
                "Only trialing, active, or past due "
                "subscriptions can be cancelled."
            )

        subscription.status = Subscription.Status.CANCELLED
        subscription.cancelled_at = timezone.now()

        subscription.save(
            update_fields=[
                "status",
                "cancelled_at",
                "updated_at",
            ]
        )

        return subscription

    @staticmethod
    @transaction.atomic
    def expire_trial(subscription):
        if (
            subscription.status
            != Subscription.Status.TRIALING
        ):
            return subscription

        if (
            subscription.trial_ends_at
            and timezone.now() >= subscription.trial_ends_at
        ):
            subscription.status = (
                Subscription.Status.EXPIRED
            )
            subscription.save(
                update_fields=[
                    "status",
                    "updated_at",
                ]
            )

        return subscription
