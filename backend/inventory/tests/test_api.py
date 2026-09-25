from decimal import Decimal

from billing.models import Plan
from billing.services.subscriptions import SubscriptionService

from django.urls import reverse
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from businesses.models import Business, BusinessMembership
from products.models import Category, Product
from suppliers.models import Supplier

from inventory.models import Purchase, StockMovement


class PurchaseAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="testpass123",
        )
        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="testpass123",
        )

        self.business = Business.objects.create(
            name="Test Liquor Store",
            phone="0712345678",
        )
        self.other_business = Business.objects.create(
            name="Other Liquor Store",
            phone="0798765432",
        )

        BusinessMembership.objects.create(
            user=self.user,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
        )
        BusinessMembership.objects.create(
            user=self.other_user,
            business=self.other_business,
            role=BusinessMembership.Role.OWNER,
        )

        plan = Plan.objects.get(
            code=Plan.Code.STARTER,
        )

        SubscriptionService.create_trial(
            business=self.business,
            plan=plan,
        )
        SubscriptionService.create_trial(
            business=self.other_business,
            plan=plan,
        )

        category = Category.objects.create(
            business=self.business,
            name="Spirits",
        )
        other_category = Category.objects.create(
            business=self.other_business,
            name="Spirits",
        )

        self.product = Product.objects.create(
            business=self.business,
            category=category,
            name="Test Vodka",
            sku="VOD-001",
            buying_price=Decimal("800.00"),
            selling_price=Decimal("1000.00"),
            stock_quantity=Decimal("10.00"),
            reorder_level=Decimal("5.00"),
        )

        self.other_product = Product.objects.create(
            business=self.other_business,
            category=other_category,
            name="Other Vodka",
            sku="OTH-001",
            buying_price=Decimal("700.00"),
            selling_price=Decimal("900.00"),
        )

        self.supplier = Supplier.objects.create(
            business=self.business,
            name="Test Distributor",
            phone="0700000000",
        )
        self.other_supplier = Supplier.objects.create(
            business=self.other_business,
            name="Other Distributor",
            phone="0700000001",
        )

        self.url = reverse(
            "purchase-list-create",
            kwargs={"business_id": self.business.id},
        )

        self.client.force_authenticate(self.user)

    def payload(
        self,
        reference="PO-001",
        supplier=None,
        product=None,
        quantity="5.00",
        unit_cost="800.00",
    ):
        return {
            "supplier": (supplier or self.supplier).id,
            "reference_number": reference,
            "purchase_date": timezone.localdate().isoformat(),
            "items": [
                {
                    "product": (product or self.product).id,
                    "quantity": quantity,
                    "unit_cost": unit_cost,
                }
            ],
        }

    def create_purchase(self, **kwargs):
        response = self.client.post(
            self.url,
            self.payload(**kwargs),
            format="json",
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        return Purchase.objects.get(
            reference_number=kwargs.get("reference", "PO-001"),
        )

    def detail_url(self, purchase):
        return reverse(
            "purchase-detail",
            kwargs={
                "business_id": purchase.business_id,
                "pk": purchase.id,
            },
        )

    def complete_url(self, purchase):
        return reverse(
            "purchase-complete",
            kwargs={
                "business_id": purchase.business_id,
                "pk": purchase.id,
            },
        )

    def cancel_url(self, purchase):
        return reverse(
            "purchase-cancel",
            kwargs={
                "business_id": purchase.business_id,
                "pk": purchase.id,
            },
        )

    def test_create_purchase(self):
        purchase = self.create_purchase()

        self.assertEqual(
            purchase.status,
            Purchase.Status.DRAFT,
        )
        self.assertEqual(
            purchase.total_amount,
            Decimal("4000.00"),
        )
        self.assertEqual(
            purchase.items.count(),
            1,
        )

    def test_list_and_retrieve_purchase(self):
        purchase = self.create_purchase()

        response = self.client.get(self.url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(response.data),
            1,
        )

        response = self.client.get(
            self.detail_url(purchase),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["reference_number"],
            "PO-001",
        )

    def test_business_isolation(self):
        Purchase.objects.create(
            business=self.other_business,
            supplier=self.other_supplier,
            created_by=self.other_user,
            reference_number="OTHER-001",
            purchase_date=timezone.localdate(),
        )

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data,
            [],
        )

    def test_invalid_supplier_is_rejected(self):
        response = self.client.post(
            self.url,
            self.payload(supplier=self.other_supplier),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_product_is_rejected(self):
        response = self.client.post(
            self.url,
            self.payload(product=self.other_product),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_items_are_rejected(self):
        response = self.client.post(
            self.url,
            self.payload(quantity="-1.00"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        data = self.payload()
        data["items"] = []

        response = self.client.post(
            self.url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_duplicate_reference_is_rejected(self):
        self.create_purchase(reference="PO-DUP")

        response = self.client.post(
            self.url,
            self.payload(reference="PO-DUP"),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_complete_purchase_updates_stock(self):
        purchase = self.create_purchase()

        response = self.client.post(
            self.complete_url(purchase),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        purchase.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(
            purchase.status,
            Purchase.Status.COMPLETED,
        )
        self.assertEqual(
            self.product.stock_quantity,
            Decimal("15.00"),
        )
        self.assertEqual(
            purchase.total_amount,
            Decimal("4000.00"),
        )

    def test_complete_purchase_creates_stock_movement(self):
        purchase = self.create_purchase()

        self.client.post(
            self.complete_url(purchase),
        )

        movement = StockMovement.objects.get(
            reference_id=purchase.id,
        )

        self.assertEqual(
            movement.product,
            self.product,
        )
        self.assertEqual(
            movement.quantity,
            Decimal("5.00"),
        )
        self.assertEqual(
            movement.movement_type,
            StockMovement.MovementType.PURCHASE,
        )
        self.assertEqual(
            movement.balance_after,
            Decimal("15.00"),
        )

    def test_purchase_cannot_be_completed_twice(self):
        purchase = self.create_purchase()

        self.client.post(
            self.complete_url(purchase),
        )

        response = self.client.post(
            self.complete_url(purchase),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cancel_purchase(self):
        purchase = self.create_purchase()

        response = self.client.post(
            self.cancel_url(purchase),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        purchase.refresh_from_db()
        self.product.refresh_from_db()

        self.assertEqual(
            purchase.status,
            Purchase.Status.CANCELLED,
        )
        self.assertEqual(
            self.product.stock_quantity,
            Decimal("10.00"),
        )
        self.assertEqual(
            StockMovement.objects.count(),
            0,
        )

    def test_cancelled_purchase_cannot_be_completed(self):
        purchase = self.create_purchase()

        self.client.post(
            self.cancel_url(purchase),
        )

        response = self.client.post(
            self.complete_url(purchase),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_completed_purchase_cannot_be_cancelled(self):
        purchase = self.create_purchase()

        self.client.post(
            self.complete_url(purchase),
        )

        response = self.client.post(
            self.cancel_url(purchase),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_unauthenticated_access_is_rejected(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
