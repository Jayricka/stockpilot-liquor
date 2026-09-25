from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from billing.models import Plan, Subscription
from businesses.models import Business, BusinessMembership


class BillingAPITestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
            first_name="John",
            last_name="Owner",
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
            is_active=True,
        )

        self.subscription = Subscription.objects.create(
            business=self.business,
            plan=self.plan,
            status=Subscription.Status.TRIALING,
            trial_started_at=timezone.now(),
            trial_ends_at=timezone.now() + timedelta(days=7),
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_plans_endpoint(self):
        response = self.client.get(
            reverse("billing-plans")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            3,
        )

        self.assertEqual(
            response.data[0]["code"],
            "starter",
        )

    def test_current_subscription_endpoint(self):
        response = self.client.get(
            reverse("current-subscription")
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
            Plan.Code.STARTER,
        )

        self.assertTrue(
            response.data["trial_active"]
        )

    def test_plans_endpoint_requires_authentication(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse("billing-plans")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_subscription_endpoint_requires_authentication(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse("current-subscription")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_subscription_requires_business_membership(self):
        other_user = User.objects.create_user(
            email="other@example.com",
            password="StrongPassword123",
        )

        self.client.force_authenticate(
            user=other_user
        )

        response = self.client.get(
            reverse("current-subscription")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
