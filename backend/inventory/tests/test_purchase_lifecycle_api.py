from decimal import Decimal

from rest_framework import status

from inventory.models import Purchase, StockMovement

from .base import PurchaseAPITestBase


class PurchaseLifecycleApiTests(PurchaseAPITestBase):

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

