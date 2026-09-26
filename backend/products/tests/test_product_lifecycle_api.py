from decimal import Decimal

from rest_framework import status

from products.models import Product

from .base import ProductAPITestBase


class ProductLifecycleApiTests(ProductAPITestBase):

        def test_product_update_does_not_change_stock(self):

            product = Product.objects.create(

                business=self.business,

                category=self.category,

                name="Stock Protected Product",

                sku="STOCK-001",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("500.00"),

                selling_price=Decimal("700.00"),

                stock_quantity=Decimal("40.00"),

                reorder_level=Decimal("5.00"),

            )

    

            response = self.client.patch(

                f"/api/businesses/{self.business.id}/products/{product.id}/",

                {

                    "name": "Updated Stock Protected Product",

                    "selling_price": "750.00",

                },

                format="json",

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_200_OK,

            )

    

            product.refresh_from_db()

    

            self.assertEqual(

                product.name,

                "Updated Stock Protected Product",

            )

    

            self.assertEqual(

                product.selling_price,

                Decimal("750.00"),

            )

    

            self.assertEqual(

                product.stock_quantity,

                Decimal("40.00"),

            )

        def test_product_update_cannot_change_opening_quantity(self):

            product = Product.objects.create(

                business=self.business,

                category=self.category,

                name="Opening Stock Product",

                sku="OPENING-001",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("500.00"),

                selling_price=Decimal("700.00"),

                stock_quantity=Decimal("20.00"),

            )

    

            response = self.client.patch(

                f"/api/businesses/{self.business.id}/products/{product.id}/",

                {

                    "initial_quantity": "100.00",

                },

                format="json",

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_400_BAD_REQUEST,

            )

    

            self.assertIn(

                "initial_quantity",

                response.data,

            )

    

            product.refresh_from_db()

    

            self.assertEqual(

                product.stock_quantity,

                Decimal("20.00"),

            )

        def test_product_can_be_deactivated(self):

            product = Product.objects.create(

                business=self.business,

                category=self.category,

                name="Active Product",

                sku="STATUS-001",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("500.00"),

                selling_price=Decimal("700.00"),

                stock_quantity=Decimal("15.00"),

                is_active=True,

            )

    

            response = self.client.patch(

                f"/api/businesses/{self.business.id}/products/{product.id}/",

                {

                    "is_active": False,

                },

                format="json",

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_200_OK,

            )

    

            product.refresh_from_db()

    

            self.assertFalse(

                product.is_active

            )

    

            self.assertEqual(

                product.stock_quantity,

                Decimal("15.00"),

            )

        def test_product_can_be_reactivated(self):

            product = Product.objects.create(

                business=self.business,

                category=self.category,

                name="Inactive Product",

                sku="STATUS-002",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("500.00"),

                selling_price=Decimal("700.00"),

                stock_quantity=Decimal("12.00"),

                is_active=False,

            )

    

            response = self.client.patch(

                f"/api/businesses/{self.business.id}/products/{product.id}/",

                {

                    "is_active": True,

                },

                format="json",

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_200_OK,

            )

    

            product.refresh_from_db()

    

            self.assertTrue(

                product.is_active

            )

    

            self.assertEqual(

                product.stock_quantity,

                Decimal("12.00"),

            )
