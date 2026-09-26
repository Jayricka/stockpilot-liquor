from decimal import Decimal

from rest_framework import status

from products.models import Product

from .base import ProductAPITestBase


class ProductsApiTests(ProductAPITestBase):

        def test_authenticated_user_can_update_product(self):

            product = Product.objects.create(

                business=self.business,

                category=self.category,

                name="Old Product Name",

                sku="UPDATE-001",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("500.00"),

                selling_price=Decimal("700.00"),

                reorder_level=Decimal("5.00"),

            )

    

            response = self.client.patch(

                f"/api/businesses/{self.business.id}/products/{product.id}/",

                {

                    "name": "Updated Product Name",

                    "selling_price": "800.00",

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

                "Updated Product Name",

            )

    

            self.assertEqual(

                product.selling_price,

                Decimal("800.00"),

            )


        def test_product_update_cannot_use_category_from_another_business(

            self,

        ):

            product = Product.objects.create(

                business=self.business,

                category=self.category,

                name="Test Product",

                sku="UPDATE-002",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("500.00"),

                selling_price=Decimal("700.00"),

            )

    

            response = self.client.patch(

                f"/api/businesses/{self.business.id}/products/{product.id}/",

                {

                    "category": self.other_category.id,

                },

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

    

            product.refresh_from_db()

    

            self.assertEqual(

                product.category_id,

                self.category.id,

            )
