from decimal import Decimal

from billing.models import Plan
from billing.services.subscriptions import SubscriptionService

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from businesses.models import Business, BusinessMembership
from inventory.models import StockMovement
from products.models import Category, Product

from sales.models import Sale


class SaleAPITests(APITestCase):

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

    def test_create_sale(self):
        sale = self.create_sale()

        self.assertEqual(
            sale.status,
            Sale.Status.DRAFT,
        )

        self.assertEqual(
            sale.items.count(),
            1,
        )

    def test_list_and_retrieve_sale(self):
        sale = self.create_sale()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        response = self.client.get(
            self.detail_url(sale),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["invoice_number"],
            "INV-001",
        )

    def test_business_isolation(self):
        response = self.client.get(
            reverse(
                "sale-list-create",
                kwargs={
                    "business_id": self.other_business.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_invalid_product_is_rejected(self):
        response = self.client.post(
            self.url,
            self.payload(
                product=self.other_product,
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_items_are_rejected(self):
        response = self.client.post(
            self.url,
            self.payload(
                quantity="-1.00",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        data = self.payload()
        data["items"] = []

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_duplicate_invoice_is_rejected(self):
        self.create_sale(invoice="INV-DUP")

        response = self.client.post(
            self.url,
            self.payload(invoice="INV-DUP"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_complete_sale_reduces_stock(self):
        sale = self.create_sale(
            quantity="2.00",
        )

        response = self.client.post(
            self.complete_url(sale),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        sale.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(
            sale.status,
            Sale.Status.COMPLETED,
        )

        self.assertEqual(
            self.product.stock_quantity,
            Decimal("8.00"),
        )

    def test_complete_sale_calculates_totals(self):
        sale = self.create_sale(
            quantity="2.00",
        )

        self.client.post(
            self.complete_url(sale),
        )

        sale.refresh_from_db()

        self.assertEqual(
            sale.subtotal,
            Decimal("2000.00"),
        )

        self.assertEqual(
            sale.total_amount,
            Decimal("2000.00"),
        )

        self.assertEqual(
            sale.total_cost,
            Decimal("1600.00"),
        )

        self.assertEqual(
            sale.gross_profit,
            Decimal("400.00"),
        )

    def test_complete_sale_creates_stock_movement(self):
        sale = self.create_sale(
            quantity="2.00",
        )

        self.client.post(
            self.complete_url(sale),
        )

        movement = StockMovement.objects.get(
            reference_id=sale.id,
        )

        self.assertEqual(
            movement.product,
            self.product,
        )

        self.assertEqual(
            movement.quantity,
            Decimal("-2.00"),
        )

        self.assertEqual(
            movement.movement_type,
            StockMovement.MovementType.SALE,
        )

        self.assertEqual(
            movement.balance_after,
            Decimal("8.00"),
        )

    def test_overselling_is_rejected(self):
        sale = self.create_sale(
            quantity="11.00",
        )

        response = self.client.post(
            self.complete_url(sale),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        sale.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(
            sale.status,
            Sale.Status.DRAFT,
        )

        self.assertEqual(
            self.product.stock_quantity,
            Decimal("10.00"),
        )

    def test_sale_cannot_be_completed_twice(self):
        sale = self.create_sale()

        self.client.post(
            self.complete_url(sale),
        )

        response = self.client.post(
            self.complete_url(sale),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cancel_sale(self):
        sale = self.create_sale()

        response = self.client.post(
            self.cancel_url(sale),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        sale.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(
            sale.status,
            Sale.Status.CANCELLED,
        )

        self.assertEqual(
            self.product.stock_quantity,
            Decimal("10.00"),
        )

    def test_cancelled_sale_cannot_be_completed(self):
        sale = self.create_sale()

        self.client.post(
            self.cancel_url(sale),
        )

        response = self.client.post(
            self.complete_url(sale),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_completed_sale_cannot_be_cancelled(self):
        sale = self.create_sale()

        self.client.post(
            self.complete_url(sale),
        )

        response = self.client.post(
            self.cancel_url(sale),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_unauthenticated_access_is_rejected(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
