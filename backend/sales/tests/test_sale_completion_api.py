from decimal import Decimal

from rest_framework import status

from inventory.models import StockMovement
from sales.models import Sale

from .base import SaleAPITestBase



class SaleCompletionApi(SaleAPITestBase):

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
