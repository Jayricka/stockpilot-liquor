from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from billing.models import Plan, Subscription
from businesses.models import Business, BusinessMembership

class DeliveryEntitlementAPITests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@test.com",
            password="TestPassword123!",
            first_name="Test",
            last_name="Owner",
        )

        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        BusinessMembership.objects.create(
            user=self.owner,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        self.starter_plan = Plan.objects.get(
            code=Plan.Code.STARTER,
            is_active=True,
        )

        self.growth_plan = Plan.objects.get(
            code=Plan.Code.GROWTH,
            is_active=True,
        )

        self.url = reverse(
            "delivery-list-create",
            kwargs={
                "business_id": self.business.id,
            },
        )

        self.client.force_authenticate(
            user=self.owner,
        )

    def create_subscription(self, plan):
        now = timezone.now()

        return Subscription.objects.create(
            business=self.business,
            plan=plan,
            status=Subscription.Status.TRIALING,
            trial_started_at=now,
            trial_ends_at=(
                now + timedelta(days=plan.trial_days)
            ),
        )

    def test_starter_plan_cannot_access_deliveries(self):
        self.create_subscription(self.starter_plan)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_growth_plan_can_access_deliveries(self):
        self.create_subscription(self.growth_plan)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_business_without_subscription_cannot_access_deliveries(
        self,
    ):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_unauthenticated_user_cannot_access_deliveries(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
