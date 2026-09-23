from decimal import Decimal

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from businesses.models import Business, BusinessMembership
from products.models import Category, Product


class ProductAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="owner@test.com",
            password="TestPassword123!",
            first_name="Test",
            last_name="Owner",
        )

        self.other_user = User.objects.create_user(
            email="other@test.com",
            password="TestPassword123!",
        )

        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        self.other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0799999999",
        )

        BusinessMembership.objects.create(
            user=self.user,
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

        self.category = Category.objects.create(
            business=self.business,
            name="Spirits",
            description="Spirits and hard liquor.",
        )

        self.other_category = Category.objects.create(
            business=self.other_business,
            name="Wine",
            description="Wine products.",
        )

        refresh = RefreshToken.for_user(self.user)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

    def product_payload(self, **overrides):
        payload = {
            "category": self.category.id,
            "name": "Smirnoff Vodka",
            "sku": "SMIRNOFF-750",
            "unit": "BOTTLE",
            "buying_price": "800.00",
            "selling_price": "1000.00",
            "reorder_level": "5.00",
            "is_active": True,
        }

        payload.update(overrides)

        return payload

    # ------------------------------------------------------------------
    # Category tests
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Product creation tests
    # ------------------------------------------------------------------

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

    def test_authenticated_user_can_create_product_with_opening_stock(self):
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

    # ------------------------------------------------------------------
    # Product list / isolation tests
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Product update tests
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Product lifecycle tests
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Product detail / isolation tests
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Delete protection
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Authentication tests
    # ------------------------------------------------------------------

    def test_unauthenticated_user_cannot_access_products(self):
        self.client.credentials()

        response = self.client.get(
            f"/api/businesses/{self.business.id}/products/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
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
