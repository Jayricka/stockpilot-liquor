from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from businesses.models import Business, BusinessMembership
from suppliers.models import Supplier

from .base import SupplierAPITestBase


class SupplierAPITests(SupplierAPITestBase):

    def test_user_cannot_see_suppliers_from_another_business(self):
            self.authenticate()

            response = self.client.get(
                self.list_url,
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
            )

            supplier_names = [
                supplier["name"]
                for supplier in response.data
            ]

            self.assertIn(
                "Kenya Drinks Distributors",
                supplier_names,
            )

            self.assertNotIn(
                "Other Drinks Supplier",
                supplier_names,
            )

    def test_supplier_detail_is_available_to_business_member(self):
            self.authenticate()

            response = self.client.get(
                self.detail_url,
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
            )

            self.assertEqual(
                response.data["name"],
                "Kenya Drinks Distributors",
            )

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
