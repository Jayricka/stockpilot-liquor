from rest_framework import status

from suppliers.models import Supplier

from .base import SupplierTestBase


class SupplierAPITests(SupplierTestBase):
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
