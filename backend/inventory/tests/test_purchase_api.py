from decimal import Decimal

from django.utils import timezone

from rest_framework import status

from inventory.models import Purchase

from .base import PurchaseAPITestBase


class PurchaseApiTests(PurchaseAPITestBase):

    def test_create_purchase(self):
        purchase = self.create_purchase()

        self.assertEqual(
            purchase.status,
            Purchase.Status.DRAFT,
        )
        self.assertEqual(
            purchase.total_amount,
            Decimal("4000.00"),
        )
        self.assertEqual(
            purchase.items.count(),
            1,
        )

    def test_list_and_retrieve_purchase(self):
        purchase = self.create_purchase()

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
            self.detail_url(purchase),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["reference_number"],
            "PO-001",
        )

    def test_business_isolation(self):
        Purchase.objects.create(
            business=self.other_business,
            supplier=self.other_supplier,
            created_by=self.other_user,
            reference_number="OTHER-001",
            purchase_date=timezone.localdate(),
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data,
            [],
        )

    def test_invalid_supplier_is_rejected(self):
        response = self.client.post(
            self.url,
            self.payload(supplier=self.other_supplier),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_product_is_rejected(self):
        response = self.client.post(
            self.url,
            self.payload(product=self.other_product),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_items_are_rejected(self):
        response = self.client.post(
            self.url,
            self.payload(quantity="-1.00"),
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

    def test_duplicate_reference_is_rejected(self):
        self.create_purchase(reference="PO-DUP")

        response = self.client.post(
            self.url,
            self.payload(reference="PO-DUP"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

