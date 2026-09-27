from decimal import Decimal

from rest_framework import status

from inventory.models import StockMovement

from .base import DemoAPITestBase


class DemoInventoryAPITests(DemoAPITestBase):
    def test_demo_purchase_increases_stock(self):
        initial_stock = self.product.stock_quantity

        response = self.client.post(
            self.purchase_url,
            {
                "product_id": self.product.id,
                "quantity": "5.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            initial_stock + Decimal("5.00"),
        )

        self.assertTrue(
            StockMovement.objects.filter(
                business=self.session.business,
                product=self.product,
                movement_type=(
                    StockMovement.MovementType.PURCHASE
                ),
                quantity=Decimal("5.00"),
            ).exists()
        )

    def test_demo_sale_decreases_stock(self):
        initial_stock = self.product.stock_quantity

        response = self.client.post(
            self.sale_url,
            {
                "product_id": self.product.id,
                "quantity": "2.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            initial_stock - Decimal("2.00"),
        )

        self.assertTrue(
            StockMovement.objects.filter(
                business=self.session.business,
                product=self.product,
                movement_type=(
                    StockMovement.MovementType.SALE
                ),
                quantity=Decimal("-2.00"),
            ).exists()
        )

    def test_demo_sale_cannot_exceed_stock(self):
        initial_stock = self.product.stock_quantity

        response = self.client.post(
            self.sale_url,
            {
                "product_id": self.product.id,
                "quantity": str(
                    initial_stock + Decimal("1.00")
                ),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            initial_stock,
        )
