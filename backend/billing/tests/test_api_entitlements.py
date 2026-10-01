from django.urls import reverse
from rest_framework import status

from billing.models import Subscription
from businesses.models import Business

from .base import BillingAPITestBase


class EntitlementListAPITests(BillingAPITestBase):

    def test_business_member_can_list_entitlements(self):
        response = self.client.get(
            reverse(
                "business-entitlements",
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
            len(response.data),
            self.plan.entitlements.count(),
        )

    def test_entitlements_return_expected_fields(self):
        response = self.client.get(
            reverse(
                "business-entitlements",
                kwargs={
                    "business_id": self.business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        entitlement = response.data[0]

        self.assertIn("feature", entitlement)
        self.assertIn("value", entitlement)

    def test_cancelled_subscription_can_access_entitlements(self):
        self.subscription.status = Subscription.Status.CANCELLED
        self.subscription.save()

        response = self.client.get(
            reverse(
                "business-entitlements",
                kwargs={
                    "business_id": self.business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_user_cannot_access_another_business_entitlements(self):
        other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0798765432",
        )

        response = self.client.get(
            reverse(
                "business-entitlements",
                kwargs={
                    "business_id": other_business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_list_entitlements(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(
            reverse(
                "business-entitlements",
                kwargs={
                    "business_id": self.business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
