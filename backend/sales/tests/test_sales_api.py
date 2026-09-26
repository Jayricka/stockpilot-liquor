from django.urls import reverse
from rest_framework import status
from sales.models import Sale

from .base import SaleAPITestBase



class SalesApi(SaleAPITestBase):

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
