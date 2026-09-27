from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from billing.models import Plan, Subscription
from billing.services.subscriptions import SubscriptionService
from businesses.models import Business

from .base import BillingPermissionTestBase


class SubscriptionPermissionServiceTests(
    BillingPermissionTestBase,
    TestCase,
):

    def test_subscription_service_expire_trial(self):
        subscription = SubscriptionService.create_trial(
            business=self.business,
            plan=self.plan,
        )

        subscription.trial_ends_at = (
            timezone.now() - timedelta(days=1)
        )
        subscription.save(
            update_fields=["trial_ends_at"]
        )

        SubscriptionService.expire_trial(subscription)

        subscription.refresh_from_db()

        self.assertEqual(
            subscription.status,
            Subscription.Status.EXPIRED,
        )
