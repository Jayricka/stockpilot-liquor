from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
from businesses.models import Business, BusinessMembership
from suppliers.models import Supplier

from .base import SupplierAPITestBase


class SupplierAPITests(SupplierAPITestBase):

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
