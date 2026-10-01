from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from billing.models import Plan, Subscription
from billing.services.subscriptions import SubscriptionService
from businesses.models import Business


class SubscriptionLifecycleTestCase(TestCase):

    def setUp(self):
        self.business = Business.objects.create(
            name="Lifecycle Liquor Store"
        )

        self.plan = Plan.objects.get(
            code=Plan.Code.STARTER
        )

        self.subscription = (
            SubscriptionService.create_trial(
                business=self.business,
                plan=self.plan,
            )
        )

    def test_activate_trial_subscription(self):
        SubscriptionService.activate(self.subscription)

        self.subscription.refresh_from_db()

        self.assertEqual(
            self.subscription.status,
            Subscription.Status.ACTIVE,
        )

    def test_activate_past_due_subscription(self):
        self.subscription.status = (
            Subscription.Status.PAST_DUE
        )
        self.subscription.save(
            update_fields=["status"]
        )

        SubscriptionService.activate(self.subscription)

        self.subscription.refresh_from_db()

        self.assertEqual(
            self.subscription.status,
            Subscription.Status.ACTIVE,
        )

    def test_activate_rejects_active_subscription(self):
        self.subscription.status = (
            Subscription.Status.ACTIVE
        )
        self.subscription.save(
            update_fields=["status"]
        )

        with self.assertRaises(ValueError):
            SubscriptionService.activate(self.subscription)

    def test_activate_rejects_cancelled_subscription(self):
        self.subscription.status = (
            Subscription.Status.CANCELLED
        )
        self.subscription.save(
            update_fields=["status"]
        )

        with self.assertRaises(ValueError):
            SubscriptionService.activate(self.subscription)

    def test_mark_past_due(self):
        self.subscription.status = (
            Subscription.Status.ACTIVE
        )
        self.subscription.save(
            update_fields=["status"]
        )

        SubscriptionService.mark_past_due(
            self.subscription
        )

        self.subscription.refresh_from_db()

        self.assertEqual(
            self.subscription.status,
            Subscription.Status.PAST_DUE,
        )

    def test_mark_past_due_rejects_trialing_subscription(
        self,
    ):
        with self.assertRaises(ValueError):
            SubscriptionService.mark_past_due(
                self.subscription
            )

    def test_cancel_trial_subscription(self):
        SubscriptionService.cancel(self.subscription)

        self.subscription.refresh_from_db()

        self.assertEqual(
            self.subscription.status,
            Subscription.Status.CANCELLED,
        )
        self.assertIsNotNone(
            self.subscription.cancelled_at
        )

    def test_cancel_active_subscription(self):
        self.subscription.status = (
            Subscription.Status.ACTIVE
        )
        self.subscription.save(
            update_fields=["status"]
        )

        SubscriptionService.cancel(self.subscription)

        self.subscription.refresh_from_db()

        self.assertEqual(
            self.subscription.status,
            Subscription.Status.CANCELLED,
        )
        self.assertIsNotNone(
            self.subscription.cancelled_at
        )

    def test_cancel_past_due_subscription(self):
        self.subscription.status = (
            Subscription.Status.PAST_DUE
        )
        self.subscription.save(
            update_fields=["status"]
        )

        SubscriptionService.cancel(self.subscription)

        self.subscription.refresh_from_db()

        self.assertEqual(
            self.subscription.status,
            Subscription.Status.CANCELLED,
        )

    def test_cancel_rejects_expired_subscription(self):
        self.subscription.status = (
            Subscription.Status.EXPIRED
        )
        self.subscription.save(
            update_fields=["status"]
        )

        with self.assertRaises(ValueError):
            SubscriptionService.cancel(self.subscription)

    def test_expire_trial(self):
        self.subscription.trial_ends_at = (
            timezone.now() - timedelta(days=1)
        )
        self.subscription.save(
            update_fields=["trial_ends_at"]
        )

        SubscriptionService.expire_trial(
            self.subscription
        )

        self.subscription.refresh_from_db()

        self.assertEqual(
            self.subscription.status,
            Subscription.Status.EXPIRED,
        )
