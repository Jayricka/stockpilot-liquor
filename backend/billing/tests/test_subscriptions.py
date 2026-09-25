from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from billing.models import Plan, Subscription
from billing.services.subscriptions import SubscriptionService
from businesses.models import Business


class SubscriptionServiceTestCase(TestCase):

    def setUp(self):
        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        self.plan = Plan.objects.get(
            code=Plan.Code.GROWTH,
            is_active=True,
        )

    def test_create_trial(self):
        subscription = (
            SubscriptionService.create_trial(
                business=self.business,
                plan=self.plan,
            )
        )

        self.assertEqual(
            subscription.business,
            self.business,
        )
        self.assertEqual(
            subscription.plan,
            self.plan,
        )
        self.assertEqual(
            subscription.status,
            Subscription.Status.TRIALING,
        )
        self.assertIsNotNone(
            subscription.trial_started_at
        )
        self.assertIsNotNone(
            subscription.trial_ends_at
        )
        self.assertTrue(
            subscription.is_trial_active
        )

    def test_create_trial_uses_plan_trial_days(self):
        subscription = (
            SubscriptionService.create_trial(
                business=self.business,
                plan=self.plan,
            )
        )

        expected_end = (
            subscription.trial_started_at
            + timedelta(days=self.plan.trial_days)
        )

        difference = abs(
            (
                subscription.trial_ends_at
                - expected_end
            ).total_seconds()
        )

        self.assertLess(
            difference,
            2,
        )

    def test_business_cannot_have_two_subscriptions(self):
        SubscriptionService.create_trial(
            business=self.business,
            plan=self.plan,
        )

        with self.assertRaises(ValueError):
            SubscriptionService.create_trial(
                business=self.business,
                plan=self.plan,
            )

        self.assertEqual(
            Subscription.objects.filter(
                business=self.business
            ).count(),
            1,
        )

    def test_expire_trial(self):
        subscription = (
            SubscriptionService.create_trial(
                business=self.business,
                plan=self.plan,
            )
        )

        subscription.trial_ends_at = (
            timezone.now() - timedelta(seconds=1)
        )
        subscription.save(
            update_fields=["trial_ends_at"]
        )

        result = SubscriptionService.expire_trial(
            subscription
        )

        self.assertEqual(
            result.status,
            Subscription.Status.EXPIRED,
        )

        result.refresh_from_db()

        self.assertEqual(
            result.status,
            Subscription.Status.EXPIRED,
        )

        self.assertFalse(
            result.is_trial_active
        )
