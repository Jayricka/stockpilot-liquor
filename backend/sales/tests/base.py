from decimal import Decimal

from billing.models import Plan
from billing.services.subscriptions import SubscriptionService

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from businesses.models import Business, BusinessMembership
from products.models import Category, Product

from sales.models import Sale


class SaleAPITestBase(APITestCase):

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
                stock_quantity=Decimal("10.00"),
            )

            self.url = reverse(
                "sale-list-create",
                kwargs={"business_id": self.business.id},
            )

            self.client.force_authenticate(self.user)

    def payload(
            self,
            invoice="INV-001",
            product=None,
            quantity="2.00",
            discount="0.00",
        ):
            return {
                "invoice_number": invoice,
                "payment_method": Sale.PaymentMethod.CASH,
                "sale_date": timezone.localdate().isoformat(),
                "discount_amount": discount,
                "notes": "",
                "items": [
                    {
                        "product": (product or self.product).id,
                        "quantity": quantity,
                    }
                ],
            }

    def create_sale(self, **kwargs):
            response = self.client.post(
                self.url,
                self.payload(**kwargs),
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
            )

            return Sale.objects.get(
                invoice_number=kwargs.get(
                    "invoice",
                    "INV-001",
                ),
            )

    def complete_url(self, sale):
            return reverse(
                "sale-complete",
                kwargs={
                    "business_id": sale.business_id,
                    "pk": sale.id,
                },
            )

    def cancel_url(self, sale):
            return reverse(
                "sale-cancel",
                kwargs={
                    "business_id": sale.business_id,
                    "pk": sale.id,
                },
            )

    def detail_url(self, sale):
            return reverse(
                "sale-detail",
                kwargs={
                    "business_id": sale.business_id,
                    "pk": sale.id,
                },
            )
