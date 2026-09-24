from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from accounts.models import User
from businesses.models import Business, BusinessMembership
from inventory.models import Purchase
from inventory.services import PurchaseService
from products.models import Category, Product
from sales.models import Sale
from sales.services import SaleService
from suppliers.models import Supplier

from .models import DemoSession


class DemoService:

    SESSION_HOURS = 24

    @staticmethod
    @transaction.atomic
    def create_session():
        demo_user = User.objects.create_user(
            email=f"demo-{timezone.now().timestamp()}@stockpilot.demo",
            password=None,
            first_name="Demo",
            last_name="User",
        )

        business = Business.objects.create(
            name="Nairobi Liquor Store",
            business_type="liquor_store",
            phone="+254 700 000 000",
            email="demo@stockpilot.demo",
            address="Nairobi, Kenya",
            license_number="DEMO-001",
        )

        BusinessMembership.objects.create(
            user=demo_user,
            business=business,
            role=BusinessMembership.Role.OWNER,
        )

        categories = DemoService._create_categories(
            business
        )

        DemoService._create_products(
            business,
            categories,
        )

        Supplier.objects.create(
            business=business,
            name="StockPilot Demo Distributors",
            phone="+254 711 000 000",
            email="supplier@stockpilot.demo",
            address="Nairobi, Kenya",
            notes="Demo supplier",
        )

        session = DemoSession.objects.create(
            user=demo_user,
            business=business,
        )

        return session

    @staticmethod
    def _create_categories(business):
        alcoholic = Category.objects.create(
            business=business,
            name="Spirits",
            group=Category.Group.ALCOHOLIC_DRINKS,
        )

        wine = Category.objects.create(
            business=business,
            name="Wine",
            group=Category.Group.ALCOHOLIC_DRINKS,
        )

        soft_drinks = Category.objects.create(
            business=business,
            name="Soft Drinks",
            group=Category.Group.SODA_AND_DRINKS,
        )

        return {
            "alcoholic": alcoholic,
            "wine": wine,
            "soft_drinks": soft_drinks,
        }

    @staticmethod
    def _create_products(
        business,
        categories,
    ):
        products = [
            {
                "category": categories["alcoholic"],
                "brand": "Jameson",
                "name": "Irish Whiskey 750ml",
                "sku": "DEMO-JAMESON-750",
                "buying_price": Decimal("2200.00"),
                "selling_price": Decimal("2800.00"),
                "stock_quantity": Decimal("18"),
                "reorder_level": Decimal("5"),
            },
            {
                "category": categories["alcoholic"],
                "brand": "Gordon's",
                "name": "London Dry Gin 750ml",
                "sku": "DEMO-GORDONS-750",
                "buying_price": Decimal("1500.00"),
                "selling_price": Decimal("1950.00"),
                "stock_quantity": Decimal("12"),
                "reorder_level": Decimal("4"),
            },
            {
                "category": categories["wine"],
                "brand": "Four Cousins",
                "name": "Sweet Red Wine 750ml",
                "sku": "DEMO-FOURCOUSINS-750",
                "buying_price": Decimal("550.00"),
                "selling_price": Decimal("800.00"),
                "stock_quantity": Decimal("8"),
                "reorder_level": Decimal("3"),
            },
            {
                "category": categories["soft_drinks"],
                "brand": "Coca-Cola",
                "name": "Coca-Cola 500ml",
                "sku": "DEMO-COKE-500",
                "buying_price": Decimal("50.00"),
                "selling_price": Decimal("80.00"),
                "stock_quantity": Decimal("25"),
                "reorder_level": Decimal("10"),
            },
        ]

        for product_data in products:
            Product.objects.create(
                business=business,
                unit=Product.Unit.BOTTLE,
                **product_data,
            )

    @staticmethod
    def is_expired(session):
        expires_at = (
            session.created_at
            + timedelta(
                hours=DemoService.SESSION_HOURS
            )
        )

        return timezone.now() >= expires_at

    @staticmethod
    def get_session(token):
        session = (
            DemoSession.objects
            .select_related(
                "user",
                "business",
            )
            .get(token=token)
        )

        if DemoService.is_expired(session):
            DemoService.delete_session(session)
            raise ValueError(
                "This demo session has expired."
            )

        return session

    @staticmethod
    @transaction.atomic
    def receive_stock(
        session,
        product_id,
        quantity,
    ):
        product = Product.objects.get(
            id=product_id,
            business=session.business,
            is_active=True,
        )

        supplier = Supplier.objects.filter(
            business=session.business,
            is_active=True,
        ).first()

        if not supplier:
            raise ValueError(
                "Demo supplier was not found."
            )

        quantity = Decimal(str(quantity))

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        reference = (
            f"DEMO-PO-{timezone.now():%Y%m%d%H%M%S%f}"
        )

        purchase = PurchaseService.create_purchase(
            business=session.business,
            user=session.user,
            validated_data={
                "supplier": supplier,
                "reference_number": reference,
                "purchase_date": timezone.localdate(),
                "notes": "Stock received in demo.",
            },
            items_data=[
                {
                    "product": product,
                    "quantity": quantity,
                    "unit_cost": product.buying_price,
                }
            ],
        )

        return PurchaseService.complete_purchase(
            purchase.id,
            session.user,
        )

    @staticmethod
    @transaction.atomic
    def make_sale(
        session,
        product_id,
        quantity,
    ):
        product = Product.objects.get(
            id=product_id,
            business=session.business,
            is_active=True,
        )

        quantity = Decimal(str(quantity))

        if quantity <= 0:
            raise ValueError(
                "Quantity must be greater than zero."
            )

        invoice = (
            f"DEMO-SALE-{timezone.now():%Y%m%d%H%M%S%f}"
        )

        sale = SaleService.create_sale(
            business=session.business,
            user=session.user,
            validated_data={
                "invoice_number": invoice,
                "payment_method": Sale.PaymentMethod.CASH,
                "sale_date": timezone.localdate(),
                "discount_amount": Decimal("0.00"),
                "notes": "Sale made in demo.",
            },
            items_data=[
                {
                    "product": product,
                    "quantity": quantity,
                }
            ],
        )

        return SaleService.complete_sale(
            sale.id,
            session.user,
        )

    @staticmethod
    @transaction.atomic
    def delete_session(session):
        business = session.business
        user = session.user

        session.delete()
        business.delete()
        user.delete()
