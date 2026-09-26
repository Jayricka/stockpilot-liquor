from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from businesses.models import Business, BusinessMembership
from suppliers.models import Supplier

from .base import SupplierAPITestBase


class SupplierAPITests(SupplierAPITestBase):

    def test_authenticated_user_can_create_supplier(self):
            self.authenticate()

            data = {
                "name": "New Drinks Supplier",
                "phone": "0722334455",
                "email": "new@supplier.com",
                "address": "Nairobi",
                "notes": "New supplier",
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
                    business=self.business,
                    name="New Drinks Supplier",
                ).count(),
                1,
            )

    def test_supplier_is_created_for_authenticated_business(self):
            self.authenticate()

            data = {
                "name": "Business Supplier",
                "phone": "0733445566",
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

            supplier = Supplier.objects.get(
                name="Business Supplier",
            )

            self.assertEqual(
                supplier.business_id,
                self.business.id,
            )

    def test_user_can_list_own_business_suppliers(self):
            self.authenticate()

            response = self.client.get(
                self.list_url,
            )

            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK,
            )

            self.assertEqual(
                len(response.data),
                1,
            )

            self.assertEqual(
                response.data[0]["name"],
                "Kenya Drinks Distributors",
            )
