from decimal import Decimal

from rest_framework import status

from products.models import Product

from .base import ProductAPITestBase


class ProductsApiTests(ProductAPITestBase):

        def test_product_detail_returns_product(self):

            product = Product.objects.create(

                business=self.business,

                category=self.category,

                name="Detailed Product",

                sku="DETAIL-001",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("900.00"),

                selling_price=Decimal("1200.00"),

                stock_quantity=Decimal("8.00"),

                reorder_level=Decimal("3.00"),

            )

    

            response = self.client.get(

                f"/api/businesses/{self.business.id}/products/{product.id}/"

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_200_OK,

            )

    

            self.assertEqual(

                response.data["name"],

                "Detailed Product",

            )

    

            self.assertEqual(

                response.data["stock_quantity"],

                "8.00",

            )

    

            self.assertEqual(

                response.data["is_low_stock"],

                False,

            )


        def test_product_cannot_be_deleted(self):

            product = Product.objects.create(

                business=self.business,

                category=self.category,

                name="Protected Product",

                sku="DELETE-001",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("500.00"),

                selling_price=Decimal("700.00"),

                stock_quantity=Decimal("10.00"),

            )

    

            response = self.client.delete(

                f"/api/businesses/{self.business.id}/products/{product.id}/"

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_405_METHOD_NOT_ALLOWED,

            )

    

            self.assertTrue(

                Product.objects.filter(

                    id=product.id,

                    business=self.business,

                ).exists()

            )
