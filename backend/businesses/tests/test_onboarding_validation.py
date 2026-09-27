from rest_framework import status

from businesses.models import Business
from billing.models import Subscription

from .base import BusinessOnboardingTestBase


class BusinessOnboardingValidationTests(BusinessOnboardingTestBase):

    def test_invalid_plan_is_rejected(self):
        response = self.client.post(
            self.url,
            self.payload("premium"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertFalse(
            Business.objects.filter(
                name="Ricka Liquor Store"
            ).exists()
        )

    def test_duplicate_business_is_rejected(self):
        response = self.client.post(
            self.url,
            self.payload("starter"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        response = self.client.post(
            self.url,
            self.payload("growth"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            Business.objects.filter(
                name="Ricka Liquor Store"
            ).count(),
            1,
        )

        self.assertEqual(
            Subscription.objects.filter(
                business__name="Ricka Liquor Store"
            ).count(),
            1,
        )

    def test_onboarding_requires_authentication(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.post(
            self.url,
            self.payload(),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
