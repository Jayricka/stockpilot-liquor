from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from accounts.models import User
from billing.models import Subscription
from businesses.models import Business, BusinessMembership

from .base import BillingAPITestBase


class BillingSubscriptionAPITest(BillingAPITestBase):

    def test_business_member_can_retrieve_subscription(self):
        response = self.client.get(
            reverse(
                "business-subscription",
                kwargs={
                    "business_id": self.business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["status"],
            Subscription.Status.TRIALING,
        )

        self.assertEqual(
            response.data["plan"]["code"],
            self.plan.code,
        )

        self.assertTrue(
            response.data["trial_active"]
        )

    def test_subscription_requires_authentication(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse(
                "business-subscription",
                kwargs={
                    "business_id": self.business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_user_cannot_access_another_business_subscription(
        self,
    ):
        other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0798765432",
        )

        Subscription.objects.create(
            business=other_business,
            plan=self.plan,
            status=Subscription.Status.TRIALING,
            trial_started_at=timezone.now(),
            trial_ends_at=(
                timezone.now()
                + timedelta(days=self.plan.trial_days)
            ),
        )

        response = self.client.get(
            reverse(
                "business-subscription",
                kwargs={
                    "business_id": other_business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_user_without_membership_cannot_access_subscription(
        self,
    ):
        other_user = User.objects.create_user(
            email="other@example.com",
            password="StrongPassword123",
        )

        self.client.force_authenticate(
            user=other_user
        )

        response = self.client.get(
            reverse(
                "business-subscription",
                kwargs={
                    "business_id": self.business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_business_without_subscription_returns_not_found(
        self,
    ):
        Subscription.objects.filter(
            business=self.business,
        ).delete()

        response = self.client.get(
            reverse(
                "business-subscription",
                kwargs={
                    "business_id": self.business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
