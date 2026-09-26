from decimal import Decimal
from rest_framework import status
from sales.models import Sale

from .base import SaleAPITestBase



class SaleLifecycleApi(SaleAPITestBase):

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
