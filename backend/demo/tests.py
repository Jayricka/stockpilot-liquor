from decimal import Decimal

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from inventory.models import StockMovement

from .services import DemoService


class DemoAPITests(APITestCase):

    def setUp(self):
        self.session = DemoService.create_session()

        self.product = (
            self.session.business.products
            .order_by("id")
            .first()
        )

        self.start_url = reverse(
            "demo-start"
        )

        self.state_url = reverse(
            "demo-state",
            kwargs={
                "token": self.session.token,
            },
        )

        self.purchase_url = reverse(
            "demo-purchase",
            kwargs={
                "token": self.session.token,
            },
        )

        self.sale_url = reverse(
            "demo-sale",
            kwargs={
                "token": self.session.token,
            },
        )

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

    def test_demo_purchase_increases_stock(self):
        initial_stock = self.product.stock_quantity

        response = self.client.post(
            self.purchase_url,
            {
                "product_id": self.product.id,
                "quantity": "5.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            initial_stock + Decimal("5.00"),
        )

        self.assertTrue(
            StockMovement.objects.filter(
                business=self.session.business,
                product=self.product,
                movement_type=(
                    StockMovement.MovementType.PURCHASE
                ),
                quantity=Decimal("5.00"),
            ).exists()
        )

    def test_demo_sale_decreases_stock(self):
        initial_stock = self.product.stock_quantity

        response = self.client.post(
            self.sale_url,
            {
                "product_id": self.product.id,
                "quantity": "2.00",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            initial_stock - Decimal("2.00"),
        )

        self.assertTrue(
            StockMovement.objects.filter(
                business=self.session.business,
                product=self.product,
                movement_type=(
                    StockMovement.MovementType.SALE
                ),
                quantity=Decimal("-2.00"),
            ).exists()
        )

    def test_demo_sale_cannot_exceed_stock(self):
        initial_stock = self.product.stock_quantity

        response = self.client.post(
            self.sale_url,
            {
                "product_id": self.product.id,
                "quantity": str(
                    initial_stock + Decimal("1.00")
                ),
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.product.refresh_from_db()

        self.assertEqual(
            self.product.stock_quantity,
            initial_stock,
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
