from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APIRequestFactory, APITestCase

from accounts.models import User
from billing.models import Plan, Subscription
from businesses.models import Business, BusinessMembership


class BillingAPITestBase(APITestCase):

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


class BillingPermissionTestBase:

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
