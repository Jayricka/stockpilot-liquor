from decimal import Decimal

from sales.models import Sale

from .base import DashboardAPITestBase


class DashboardDataApiTests(DashboardAPITestBase):

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

