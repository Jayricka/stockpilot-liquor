from decimal import Decimal

from django.urls import reverse
from rest_framework import status

from demo.services import DemoService

from .base import DemoAPITestBase


class DemoSessionAPITests(DemoAPITestBase):
    def test_demo_session_contains_products(self):
        response = self.client.get(
            self.state_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["business"]["name"],
            "Nairobi Liquor Store",
        )

        self.assertEqual(
            len(response.data["products"]),
            4,
        )

    def test_demo_sessions_are_isolated(self):
        second_session = (
            DemoService.create_session()
        )

        first_product = (
            self.session.business.products
            .order_by("id")
            .first()
        )

        second_product = (
            second_session.business.products
            .order_by("id")
            .first()
        )

        self.assertNotEqual(
            self.session.business.id,
            second_session.business.id,
        )

        self.assertNotEqual(
            first_product.id,
            second_product.id,
        )

        first_stock = first_product.stock_quantity

        response = self.client.post(
            reverse(
                "demo-sale",
                kwargs={
                    "token": self.session.token,
                },
            ),
            {
                "product_id": first_product.id,
                "quantity": "1.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        first_product.refresh_from_db()
        second_product.refresh_from_db()

        self.assertEqual(
            first_product.stock_quantity,
            first_stock - Decimal("1.00"),
        )

        self.assertEqual(
            second_product.stock_quantity,
            Decimal("18.00"),
        )

    def test_demo_start_creates_new_session(self):
        response = self.client.post(
            self.start_url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertIn(
            "token",
            response.data,
        )

        self.assertIn(
            "business",
            response.data,
        )
