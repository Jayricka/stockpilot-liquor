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
