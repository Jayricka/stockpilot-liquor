from decimal import Decimal

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from businesses.models import Business, BusinessMembership
from deliveries.models import DeliveryOrder
from inventory.models import Purchase, PurchaseItem
from products.models import Category, Product
from sales.models import Sale, SaleItem
from suppliers.models import Supplier


class DashboardAPITests(APITestCase):

    def setUp(self):
        self.owner = User.objects.create_user(
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
            phone="0798765432",
        )

        BusinessMembership.objects.create(
            user=self.owner,
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

        self.category = Category.objects.create(
            business=self.business,
            name="Spirits",
        )

        self.product = Product.objects.create(
            business=self.business,
            category=self.category,
            name="Test Vodka",
            sku="VOD-001",
            unit=Product.Unit.BOTTLE,
            buying_price=Decimal("1000.00"),
            selling_price=Decimal("1500.00"),
            stock_quantity=Decimal("10.00"),
            reorder_level=Decimal("3.00"),
        )

        self.low_stock_product = Product.objects.create(
            business=self.business,
            category=self.category,
            name="Low Stock Gin",
            sku="GIN-001",
            unit=Product.Unit.BOTTLE,
            buying_price=Decimal("800.00"),
            selling_price=Decimal("1200.00"),
            stock_quantity=Decimal("2.00"),
            reorder_level=Decimal("5.00"),
        )

        self.other_category = Category.objects.create(
            business=self.other_business,
            name="Other Spirits",
        )

        Product.objects.create(
            business=self.other_business,
            category=self.other_category,
            name="Other Vodka",
            sku="OTHER-001",
            unit=Product.Unit.BOTTLE,
            buying_price=Decimal("900.00"),
            selling_price=Decimal("1300.00"),
            stock_quantity=Decimal("20.00"),
            reorder_level=Decimal("5.00"),
        )

        self.sale = Sale.objects.create(
            business=self.business,
            created_by=self.owner,
            invoice_number="INV-001",
            payment_method=Sale.PaymentMethod.MPESA,
            status=Sale.Status.COMPLETED,
            sale_date=timezone.now(),
            subtotal=Decimal("3000.00"),
            total_amount=Decimal("3000.00"),
            total_cost=Decimal("2000.00"),
            gross_profit=Decimal("1000.00"),
        )

        SaleItem.objects.create(
            sale=self.sale,
            product=self.product,
            quantity=Decimal("2.00"),
            unit_price=Decimal("1500.00"),
            unit_cost=Decimal("1000.00"),
        )

        self.supplier = Supplier.objects.create(
            business=self.business,
            name="Test Supplier",
            phone="0711223344",
        )

        self.purchase = Purchase.objects.create(
            business=self.business,
            supplier=self.supplier,
            created_by=self.owner,
            reference_number="PUR-001",
            status=Purchase.Status.COMPLETED,
            purchase_date=timezone.now(),
            total_amount=Decimal("2000.00"),
        )

        PurchaseItem.objects.create(
            purchase=self.purchase,
            product=self.product,
            quantity=Decimal("2.00"),
            unit_cost=Decimal("1000.00"),
        )

        self.delivery = DeliveryOrder.objects.create(
            business=self.business,
            sale=self.sale,
            customer_name="Test Customer",
            customer_phone="0700000000",
            delivery_address="Nairobi",
            delivery_fee=Decimal("200.00"),
            status=DeliveryOrder.Status.PENDING,
        )

        self.url = reverse(
            "dashboard",
            kwargs={
                "business_id": self.business.id,
            },
        )

    def authenticate(self):
        self.client.force_authenticate(
            user=self.owner,
        )

    def test_authenticated_user_can_access_dashboard(self):
        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_dashboard_contains_summary(self):
        self.authenticate()

        response = self.client.get(self.url)

        summary = response.data["summary"]

        self.assertEqual(
            summary["today_sales_count"],
            1,
        )

        self.assertEqual(
            Decimal(str(summary["today_revenue"])),
            Decimal("3000.00"),
        )

        self.assertEqual(
            Decimal(str(summary["today_gross_profit"])),
            Decimal("1000.00"),
        )

    def test_dashboard_contains_stock_metrics(self):
        self.authenticate()

        response = self.client.get(self.url)

        summary = response.data["summary"]

        self.assertEqual(
            summary["total_products"],
            2,
        )

        self.assertEqual(
            summary["low_stock_count"],
            1,
        )

        self.assertEqual(
            Decimal(str(summary["total_stock_value"])),
            Decimal("11600.00"),
        )

    def test_dashboard_contains_pending_delivery_count(self):
        self.authenticate()

        response = self.client.get(self.url)

        self.assertEqual(
            response.data["summary"]["pending_delivery_count"],
            1,
        )

    def test_dashboard_contains_payment_method_summary(self):
        self.authenticate()

        response = self.client.get(self.url)

        payments = response.data["sales_by_payment_method"]

        self.assertEqual(
            len(payments),
            1,
        )

        self.assertEqual(
            payments[0]["payment_method"],
            Sale.PaymentMethod.MPESA,
        )

        self.assertEqual(
            Decimal(str(payments[0]["total"])),
            Decimal("3000.00"),
        )

    def test_dashboard_contains_top_products(self):
        self.authenticate()

        response = self.client.get(self.url)

        products = response.data["top_products"]

        self.assertEqual(
            len(products),
            1,
        )

        self.assertEqual(
            products[0]["items__product__name"],
            "Test Vodka",
        )

        self.assertEqual(
            Decimal(str(products[0]["quantity"])),
            Decimal("2.00"),
        )

    def test_dashboard_contains_low_stock_products(self):
        self.authenticate()

        response = self.client.get(self.url)

        products = response.data["low_stock_products"]

        self.assertEqual(
            len(products),
            1,
        )

        self.assertEqual(
            products[0]["name"],
            "Low Stock Gin",
        )

    def test_dashboard_contains_recent_sales(self):
        self.authenticate()

        response = self.client.get(self.url)

        sales = response.data["recent_sales"]

        self.assertEqual(
            len(sales),
            1,
        )

        self.assertEqual(
            sales[0]["invoice_number"],
            "INV-001",
        )

    def test_dashboard_contains_recent_purchases(self):
        self.authenticate()

        response = self.client.get(self.url)

        purchases = response.data["recent_purchases"]

        self.assertEqual(
            len(purchases),
            1,
        )

        self.assertEqual(
            purchases[0]["reference_number"],
            "PUR-001",
        )

    def test_dashboard_is_business_isolated(self):
        self.authenticate()

        response = self.client.get(self.url)

        response_text = str(response.data)

        self.assertNotIn(
            "Other Vodka",
            response_text,
        )

    def test_user_cannot_access_another_business_dashboard(self):
        self.authenticate()

        url = reverse(
            "dashboard",
            kwargs={
                "business_id": self.other_business.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_access_dashboard(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
