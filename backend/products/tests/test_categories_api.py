from decimal import Decimal

from rest_framework import status

from products.models import Category, Product

from .base import ProductAPITestBase


class CategoriesApiTests(ProductAPITestBase):

        def test_authenticated_user_can_create_category(self):

            response = self.client.post(

                f"/api/businesses/{self.business.id}/categories/",

                {

                    "name": "Wine",

                    "description": "Wine products.",

                },

                format="json",

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_201_CREATED,

            )

    

            category = Category.objects.get(

                business=self.business,

                name="Wine",

            )

    

            self.assertEqual(

                response.data["id"],

                category.id,

            )

    

            self.assertEqual(

                response.data["name"],

                "Wine",

            )

        def test_authenticated_user_can_list_categories(self):

            response = self.client.get(

                f"/api/businesses/{self.business.id}/categories/"

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

                "Spirits",

            )

        def test_user_cannot_access_categories_from_another_business(self):

            response = self.client.get(

                f"/api/businesses/{self.other_business.id}/categories/"

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_404_NOT_FOUND,

            )

        def test_unauthenticated_user_cannot_access_categories(self):

            self.client.credentials()

    

            response = self.client.get(

                f"/api/businesses/{self.business.id}/categories/"

            )

    

            self.assertEqual(

                response.status_code,

                status.HTTP_401_UNAUTHORIZED,

            )
