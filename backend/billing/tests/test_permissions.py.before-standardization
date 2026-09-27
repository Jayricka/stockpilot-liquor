from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView

from businesses.models import Business, BusinessMembership

from billing.models import Plan, Subscription
from billing.permissions import HasOperationalAccess
from billing.services.subscriptions import SubscriptionService

from django.test import TestCase


User = get_user_model()


class HasOperationalAccessTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="testpassword123",
        )

        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        BusinessMembership.objects.create(
            user=self.user,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        self.plan = Plan.objects.get(
            code=Plan.Code.STARTER,
        )

        self.factory = APIRequestFactory()
        self.permission = HasOperationalAccess()

        self.view = APIView()
        self.view.kwargs = {
            "business_id": self.business.id,
        }

    def get_request(self):
        request = self.factory.get(
            f"/businesses/{self.business.id}/products/",
        )
        request.user = self.user
        return request

    def create_subscription(
        self,
        status=Subscription.Status.TRIALING,
    ):
        now = timezone.now()

        return Subscription.objects.create(
            business=self.business,
            plan=self.plan,
            status=status,
            trial_started_at=now,
            trial_ends_at=(
                now + timedelta(days=self.plan.trial_days)
            ),
        )

    def test_active_subscription_is_allowed(self):
        self.create_subscription(
            status=Subscription.Status.ACTIVE,
        )

        request = self.get_request()

        self.assertTrue(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_active_trial_is_allowed(self):
        self.create_subscription()

        request = self.get_request()

        self.assertTrue(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_expired_trial_is_blocked(self):
        subscription = self.create_subscription()

        subscription.trial_ends_at = (
            timezone.now() - timedelta(days=1)
        )
        subscription.save(
            update_fields=["trial_ends_at"]
        )

        request = self.get_request()

        self.assertFalse(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

        subscription.refresh_from_db()

        self.assertEqual(
            subscription.status,
            Subscription.Status.EXPIRED,
        )

    def test_expired_subscription_is_blocked(self):
        self.create_subscription(
            status=Subscription.Status.EXPIRED,
        )

        request = self.get_request()

        self.assertFalse(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_cancelled_subscription_is_blocked(self):
        self.create_subscription(
            status=Subscription.Status.CANCELLED,
        )

        request = self.get_request()

        self.assertFalse(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_past_due_subscription_is_blocked(self):
        self.create_subscription(
            status=Subscription.Status.PAST_DUE,
        )

        request = self.get_request()

        self.assertFalse(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_missing_subscription_is_blocked(self):
        request = self.get_request()

        self.assertFalse(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

    def test_inactive_membership_does_not_block_queryset_access(self):
        BusinessMembership.objects.filter(
            user=self.user,
            business=self.business,
        ).update(is_active=False)

        request = self.get_request()

        self.assertTrue(
            self.permission.has_permission(
                request,
                self.view,
            )
        )

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
