from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from billing.models import Payment, Plan, Subscription
from businesses.models import Business


class BillingModelTestCase(TestCase):

    def setUp(self):
        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        self.plan = Plan.objects.get(
            code=Plan.Code.STARTER,
            is_active=True,
        )

    def test_plan_creation(self):
        self.assertEqual(
            self.plan.code,
            Plan.Code.STARTER,
        )
        self.assertEqual(
            self.plan.name,
            "Starter",
        )
        self.assertEqual(
            self.plan.price,
            999,
        )
        self.assertEqual(
            self.plan.currency,
            "KES",
        )
        self.assertEqual(
            self.plan.trial_days,
            7,
        )
        self.assertTrue(
            self.plan.is_active,
        )

    def test_subscription_trial_is_active(self):
        now = timezone.now()

        subscription = Subscription.objects.create(
            business=self.business,
            plan=self.plan,
            status=Subscription.Status.TRIALING,
            trial_started_at=now,
            trial_ends_at=now + timedelta(days=7),
        )

        self.assertTrue(
            subscription.is_trial_active
        )

        self.assertGreater(
            subscription.trial_days_remaining,
            0,
        )

    def test_expired_trial_is_not_active(self):
        now = timezone.now()

        subscription = Subscription.objects.create(
            business=self.business,
            plan=self.plan,
            status=Subscription.Status.TRIALING,
            trial_started_at=now - timedelta(days=8),
            trial_ends_at=now - timedelta(days=1),
        )

        self.assertFalse(
            subscription.is_trial_active
        )

        self.assertEqual(
            subscription.trial_days_remaining,
            0,
        )

    def test_payment_defaults_to_pending(self):
        subscription = Subscription.objects.create(
            business=self.business,
            plan=self.plan,
            status=Subscription.Status.TRIALING,
            trial_started_at=timezone.now(),
            trial_ends_at=timezone.now() + timedelta(days=7),
        )

        payment = Payment.objects.create(
            subscription=subscription,
            amount=self.plan.price,
            currency="KES",
            phone_number="0712345678",
        )

        self.assertEqual(
            payment.status,
            Payment.Status.PENDING,
        )
        self.assertEqual(
            payment.amount,
            999,
        )
        self.assertEqual(
            payment.currency,
            "KES",
        )
