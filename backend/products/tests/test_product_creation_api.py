from decimal import Decimal

from rest_framework import status

from products.models import Product

from .base import ProductAPITestBase


class ProductsApiTests(ProductAPITestBase):

        def test_authenticated_user_can_create_product(self):

            response = self.client.post(

                f"/api/businesses/{self.business.id}/products/",

                self.product_payload(),

                format="json",

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_201_CREATED,

            )

    

            product = Product.objects.get(

                business=self.business,

                sku="SMIRNOFF-750",

            )

    

            self.assertEqual(

                product.name,

                "Smirnoff Vodka",

            )

    

            self.assertEqual(

                product.stock_quantity,

                Decimal("0.00"),

            )

    

            self.assertEqual(

                product.buying_price,

                Decimal("800.00"),

            )

    

            self.assertEqual(

                product.selling_price,

                Decimal("1000.00"),

            )

    

            self.assertEqual(

                response.data["category_name"],

                "Spirits",

            )


        def test_authenticated_user_can_create_product_with_opening_stock(

            self,

        ):

            response = self.client.post(

                f"/api/businesses/{self.business.id}/products/",

                self.product_payload(

                    initial_quantity="25.00",

                ),

                format="json",

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_201_CREATED,

            )

    

            product = Product.objects.get(

                business=self.business,

                sku="SMIRNOFF-750",

            )

    

            self.assertEqual(

                product.stock_quantity,

                Decimal("25.00"),

            )

    

            self.assertEqual(

                response.data["stock_quantity"],

                "25.00",

            )


        def test_product_cannot_use_category_from_another_business(self):

            response = self.client.post(

                f"/api/businesses/{self.business.id}/products/",

                self.product_payload(

                    category=self.other_category.id,

                ),

                format="json",

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_400_BAD_REQUEST,

            )

    

            self.assertIn(

                "detail",

                response.data,

            )

    

            self.assertEqual(

                response.data["detail"],

                "Category does not belong to this business.",

            )

    

            self.assertFalse(

                Product.objects.filter(

                    business=self.business

                ).exists()

            )


        def test_selling_price_cannot_be_lower_than_buying_price(self):

            response = self.client.post(

                f"/api/businesses/{self.business.id}/products/",

                self.product_payload(

                    buying_price="1000.00",

                    selling_price="800.00",

                ),

                format="json",

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_400_BAD_REQUEST,

            )

    

            self.assertIn(

                "selling_price",

                response.data,

            )

    

            self.assertEqual(

                response.data["selling_price"][0],

                "Selling price cannot be lower than buying price.",

            )
