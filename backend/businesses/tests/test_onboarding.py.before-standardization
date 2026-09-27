from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from billing.models import Plan, Subscription
from businesses.models import (
    Business,
    BusinessMembership,
)


class BusinessOnboardingTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
            first_name="John",
            last_name="Owner",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.url = reverse(
            "business-onboard"
        )

    def payload(self, plan="starter"):
        return {
            "name": "Ricka Liquor Store",
            "business_type": "liquor_store",
            "phone": "0712345678",
            "email": "store@example.com",
            "address": "Nairobi",
            "license_number": "LIC-12345",
            "plan": plan,
        }

    def test_onboarding_creates_business_and_trial(self):
        response = self.client.post(
            self.url,
            self.payload("growth"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        business = Business.objects.get(
            name="Ricka Liquor Store"
        )

        subscription = Subscription.objects.get(
            business=business
        )

        growth_plan = Plan.objects.get(
            code=Plan.Code.GROWTH
        )

        self.assertEqual(
            subscription.plan,
            growth_plan,
        )

        self.assertEqual(
            subscription.status,
            Subscription.Status.TRIALING,
        )

        self.assertTrue(
            subscription.is_trial_active
        )

        self.assertEqual(
            response.data["subscription"]["plan"]["code"],
            "growth",
        )

        self.assertEqual(
            response.data["subscription"]["plan"]["price"],
            1999,
        )

    def test_onboarding_creates_owner_membership(self):
        response = self.client.post(
            self.url,
            self.payload("starter"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        business = Business.objects.get(
            name="Ricka Liquor Store"
        )

        membership = BusinessMembership.objects.get(
            user=self.user,
            business=business,
        )

        self.assertEqual(
            membership.role,
            BusinessMembership.Role.OWNER,
        )

        self.assertTrue(
            membership.is_active
        )

    def test_onboarding_uses_plan_trial_days(self):
        response = self.client.post(
            self.url,
            self.payload("business"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        business = Business.objects.get(
            name="Ricka Liquor Store"
        )

        subscription = Subscription.objects.get(
            business=business
        )

        expected_end = (
            subscription.trial_started_at
            + timedelta(
                days=subscription.plan.trial_days
            )
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
