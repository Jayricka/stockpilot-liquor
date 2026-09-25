from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from businesses.models import Business, BusinessMembership
from suppliers.models import Supplier


class SupplierAPITests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@test.com",
            password="TestPassword123!",
            first_name="Test",
            last_name="Owner",
        )

        self.other_user = User.objects.create_user(
            email="other@test.com",
            password="TestPassword123!",
            first_name="Other",
            last_name="User",
        )

        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        self.other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0798765432",
        )

        BusinessMembership.objects.create(
            user=self.owner,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        BusinessMembership.objects.create(
            user=self.other_user,
            business=self.other_business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        self.supplier = Supplier.objects.create(
            business=self.business,
            name="Kenya Drinks Distributors",
            phone="0711223344",
            email="supplier@test.com",
            address="Nairobi",
            notes="Main drinks supplier",
        )

        self.other_supplier = Supplier.objects.create(
            business=self.other_business,
            name="Other Drinks Supplier",
            phone="0700000000",
            email="other@supplier.com",
            address="Nairobi",
            notes="Other business supplier",
        )

        self.list_url = reverse(
            "supplier-list-create",
            kwargs={"business_id": self.business.id},
        )

        self.detail_url = reverse(
            "supplier-detail",
            kwargs={
                "business_id": self.business.id,
                "pk": self.supplier.id,
            },
        )

    def authenticate(self):
        self.client.force_authenticate(user=self.owner)

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
