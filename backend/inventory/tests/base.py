from decimal import Decimal

from billing.models import Plan
from billing.services.subscriptions import SubscriptionService

from django.urls import reverse
from django.utils import timezone

from rest_framework.test import APITestCase

from accounts.models import User
from businesses.models import Business, BusinessMembership
from products.models import Category, Product
from suppliers.models import Supplier

from inventory.models import Purchase


class PurchaseTestBase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123",
        )

        self.business = Business.objects.create(
            name="Test Liquor Store",
            phone="0712345678",
        )
        self.other_business = Business.objects.create(
            name="Other Liquor Store",
            phone="0798765432",
        )

        BusinessMembership.objects.create(
            user=self.user,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
        )
        BusinessMembership.objects.create(
            user=self.other_user,
            business=self.other_business,
            role=BusinessMembership.Role.OWNER,
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

        category = Category.objects.create(
            business=self.business,
            name="Spirits",
        )
        other_category = Category.objects.create(
            business=self.other_business,
            name="Spirits",
        )

        self.product = Product.objects.create(
            business=self.business,
            category=category,
            name="Test Vodka",
            sku="VOD-001",
            buying_price=Decimal("800.00"),
            selling_price=Decimal("1000.00"),
            stock_quantity=Decimal("10.00"),
            reorder_level=Decimal("5.00"),
        )

        self.other_product = Product.objects.create(
            business=self.other_business,
            category=other_category,
            name="Other Vodka",
            sku="OTH-001",
            buying_price=Decimal("700.00"),
            selling_price=Decimal("900.00"),
        )

        self.supplier = Supplier.objects.create(
            business=self.business,
            name="Test Distributor",
            phone="0700000000",
        )
        self.other_supplier = Supplier.objects.create(
            business=self.other_business,
            name="Other Distributor",
            phone="0700000001",
        )

        self.url = reverse(
            "purchase-list-create",
            kwargs={"business_id": self.business.id},
        )

        self.client.force_authenticate(self.user)

    def payload(
        self,
        reference="PO-001",
        supplier=None,
        product=None,
        quantity="5.00",
        unit_cost="800.00",
    ):
        return {
            "supplier": (supplier or self.supplier).id,
            "reference_number": reference,
            "purchase_date": timezone.localdate().isoformat(),
            "items": [
                {
                    "product": (product or self.product).id,
                    "quantity": quantity,
                    "unit_cost": unit_cost,
                }
            ],
        }

    def create_purchase(self, **kwargs):
        response = self.client.post(
            self.url,
            self.payload(**kwargs),
            format="json",
        )
        self.assertEqual(
            response.status_code,
            201,
        )
        return Purchase.objects.get(
            reference_number=kwargs.get("reference", "PO-001"),
        )

    def detail_url(self, purchase):
        return reverse(
            "purchase-detail",
            kwargs={
                "business_id": purchase.business_id,
                "pk": purchase.id,
            },
        )

    def complete_url(self, purchase):
        return reverse(
            "purchase-complete",
            kwargs={
                "business_id": purchase.business_id,
                "pk": purchase.id,
            },
        )

    def cancel_url(self, purchase):
        return reverse(
            "purchase-cancel",
            kwargs={
                "business_id": purchase.business_id,
                "pk": purchase.id,
            },
        )
