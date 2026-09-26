from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from businesses.models import Business, BusinessMembership
from suppliers.models import Supplier

from .base import SupplierAPITestBase


class SupplierAPITests(SupplierAPITestBase):

    def test_duplicate_supplier_name_is_rejected_for_same_business(self):
            self.authenticate()

            data = {
                "name": "Kenya Drinks Distributors",
                "phone": "0744556677",
            }

            response = self.client.post(
                self.list_url,
                data,
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST,
            )

    def test_same_supplier_name_can_exist_in_different_businesses(self):
            self.authenticate()

            data = {
                "name": "Other Drinks Supplier",
                "phone": "0755667788",
            }

            response = self.client.post(
                self.list_url,
                data,
                format="json",
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED,
            )

            self.assertEqual(
                Supplier.objects.filter(
                    name="Other Drinks Supplier",
                ).count(),
                2,
            )
