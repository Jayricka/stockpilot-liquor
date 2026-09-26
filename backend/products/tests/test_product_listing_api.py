from decimal import Decimal

from rest_framework import status

from products.models import Product

from .base import ProductAPITestBase


class ProductsApiTests(ProductAPITestBase):

        def test_authenticated_user_can_list_products(self):

            Product.objects.create(

                business=self.business,

                category=self.category,

                name="Johnnie Walker",

                sku="JW-750",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("1500.00"),

                selling_price=Decimal("2000.00"),

                stock_quantity=Decimal("10.00"),

                reorder_level=Decimal("3.00"),

            )

    

            response = self.client.get(

                f"/api/businesses/{self.business.id}/products/"

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

                "Johnnie Walker",

            )

    

            self.assertEqual(

                response.data[0]["category_name"],

                "Spirits",

            )

    

            self.assertEqual(

                response.data[0]["stock_quantity"],

                "10.00",

            )


        def test_user_can_only_see_products_from_their_business(self):

            own_product = Product.objects.create(

                business=self.business,

                category=self.category,

                name="Own Product",

                sku="OWN-001",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("500.00"),

                selling_price=Decimal("700.00"),

            )

    

            Product.objects.create(

                business=self.other_business,

                category=self.other_category,

                name="Other Product",

                sku="OTHER-001",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("600.00"),

                selling_price=Decimal("800.00"),

            )

    

            response = self.client.get(

                f"/api/businesses/{self.business.id}/products/"

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

                response.data[0]["id"],

                own_product.id,

            )

    

            self.assertEqual(

                response.data[0]["name"],

                "Own Product",

            )
