from decimal import Decimal

from rest_framework import status

from .base import DashboardAPITestBase


class DashboardApiTests(DashboardAPITestBase):

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

