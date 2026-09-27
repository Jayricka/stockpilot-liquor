from decimal import Decimal

from rest_framework import status

from inventory.models import Purchase, StockMovement

from .base import PurchaseTestBase


class PurchaseLifecycleAPITests(PurchaseTestBase):

    def test_complete_purchase_updates_stock(self):
        purchase = self.create_purchase()

        response = self.client.post(
            self.complete_url(purchase),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        purchase.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(
            purchase.status,
            Purchase.Status.COMPLETED,
        )
        self.assertEqual(
            self.product.stock_quantity,
            Decimal("15.00"),
        )
        self.assertEqual(
            purchase.total_amount,
            Decimal("4000.00"),
        )

    def test_complete_purchase_creates_stock_movement(self):
        purchase = self.create_purchase()

        self.client.post(
            self.complete_url(purchase),
        )

        movement = StockMovement.objects.get(
            reference_id=purchase.id,
        )

        self.assertEqual(
            movement.product,
            self.product,
        )
        self.assertEqual(
            movement.quantity,
            Decimal("5.00"),
        )
        self.assertEqual(
            movement.movement_type,
            StockMovement.MovementType.PURCHASE,
        )
        self.assertEqual(
            movement.balance_after,
            Decimal("15.00"),
        )

    def test_purchase_cannot_be_completed_twice(self):
        purchase = self.create_purchase()

        self.client.post(
            self.complete_url(purchase),
        )

        response = self.client.post(
            self.complete_url(purchase),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cancel_purchase(self):
        purchase = self.create_purchase()

        response = self.client.post(
            self.cancel_url(purchase),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        purchase.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(
            purchase.status,
            Purchase.Status.CANCELLED,
        )
        self.assertEqual(
            self.product.stock_quantity,
            Decimal("10.00"),
        )
        self.assertEqual(
            StockMovement.objects.count(),
            0,
        )

    def test_cancelled_purchase_cannot_be_completed(self):
        purchase = self.create_purchase()

        self.client.post(
            self.cancel_url(purchase),
        )

        response = self.client.post(
            self.complete_url(purchase),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_completed_purchase_cannot_be_cancelled(self):
        purchase = self.create_purchase()

        self.client.post(
            self.complete_url(purchase),
        )

        response = self.client.post(
            self.cancel_url(purchase),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
