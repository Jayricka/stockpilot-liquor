from django.urls import reverse
from rest_framework import status

from .base import SupplierTestBase


class SupplierAPIAccessTests(SupplierTestBase):
    def test_supplier_from_another_business_is_not_accessible(self):
        self.authenticate()

        url = reverse(
            "supplier-detail",
            kwargs={
                "business_id": self.business.id,
                "pk": self.other_supplier.id,
            },
        )

        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_list_suppliers(self):
        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_unauthenticated_user_cannot_create_supplier(self):
        data = {
            "name": "Unauthorised Supplier",
            "phone": "0711111111",
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
