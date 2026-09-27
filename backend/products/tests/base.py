from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from billing.models import Plan
from billing.services.subscriptions import SubscriptionService
from businesses.models import Business, BusinessMembership
from products.models import Category


class ProductTestBase:

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="owner@test.com",
            password="TestPassword123!",
            first_name="Test",
            last_name="Owner",
        )

        self.other_user = User.objects.create_user(
            email="other@test.com",
            password="TestPassword123!",
        )

        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        self.other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0799999999",
        )

        BusinessMembership.objects.create(
            user=self.user,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        BusinessMembership.objects.create(
            user=self.other_user,
            business=self.other_business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        plan = Plan.objects.get(
            code=Plan.Code.STARTER,
        )

        SubscriptionService.create_trial(
            business=self.business,
            plan=plan,
        )

        SubscriptionService.create_trial(
            business=self.other_business,
            plan=plan,
        )

        self.category = Category.objects.create(
            business=self.business,
            name="Spirits",
            description="Spirits and hard liquor.",
        )

        self.other_category = Category.objects.create(
            business=self.other_business,
            name="Wine",
            description="Wine products.",
        )

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

    def product_payload(self, **overrides):
        payload = {
            "category": self.category.id,
            "name": "Smirnoff Vodka",
            "sku": "SMIRNOFF-750",
            "unit": "BOTTLE",
            "buying_price": "800.00",
            "selling_price": "1000.00",
            "reorder_level": "5.00",
            "is_active": True,
        }

        payload.update(overrides)

        return payload
