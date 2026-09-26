from decimal import Decimal

from rest_framework import status

from products.models import Product

from .base import ProductAPITestBase


class ProductPermissionsApiTests(ProductAPITestBase):

        def test_user_cannot_access_product_from_another_business(self):

            product = Product.objects.create(

                business=self.other_business,

                category=self.other_category,

                name="Private Product",

                sku="PRIVATE-001",

                unit=Product.Unit.BOTTLE,

                buying_price=Decimal("500.00"),

                selling_price=Decimal("700.00"),

            )

    

            response = self.client.get(

                f"/api/businesses/{self.business.id}/products/{product.id}/"

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_404_NOT_FOUND,

            )

        def test_unauthenticated_user_cannot_access_products(self):

            self.client.credentials()

    

            response = self.client.get(

                f"/api/businesses/{self.business.id}/products/"

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_401_UNAUTHORIZED,

            )
