from django.urls import reverse
from rest_framework import status

from billing.models import Payment, Subscription
from businesses.models import Business

from .base import BillingAPITestBase


class PaymentDetailAPITests(BillingAPITestBase):

    def setUp(self):
        super().setUp()

        self.payment = Payment.objects.create(
            subscription=self.subscription,
            amount=1500,
            currency="KES",
            phone_number="0712345678",
            status=Payment.Status.SUCCESS,
            mpesa_receipt="QWE123456",
        )

        self.url = reverse(
            "business-payment-detail",
            kwargs={
                "business_id": self.business.id,
                "payment_id": self.payment.id,
            },
        )

    def test_business_member_can_retrieve_payment(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["id"],
            self.payment.id,
        )

    def test_payment_returns_expected_fields(self):
        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data["amount"],
            1500,
        )
        self.assertEqual(
            response.data["currency"],
            "KES",
        )
        self.assertEqual(
            response.data["phone_number"],
            "0712345678",
        )
        self.assertEqual(
            response.data["status"],
            Payment.Status.SUCCESS,
        )
        self.assertEqual(
            response.data["mpesa_receipt"],
            "QWE123456",
        )

    def test_user_cannot_access_payment_from_another_business(
        self,
    ):
        other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0798765432",
        )

        other_subscription = Subscription.objects.create(
            business=other_business,
            plan=self.plan,
            status=self.subscription.status,
            trial_started_at=(
                self.subscription.trial_started_at
            ),
            trial_ends_at=(
                self.subscription.trial_ends_at
            ),
        )

        other_payment = Payment.objects.create(
            subscription=other_subscription,
            amount=2000,
            currency="KES",
            phone_number="0798765432",
            status=Payment.Status.SUCCESS,
        )

        response = self.client.get(
            reverse(
                "business-payment-detail",
                kwargs={
                    "business_id": other_business.id,
                    "payment_id": other_payment.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_nonexistent_payment_returns_404(self):
        response = self.client.get(
            reverse(
                "business-payment-detail",
                kwargs={
                    "business_id": self.business.id,
                    "payment_id": 999999,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_user_cannot_access_payment_through_another_business_id(
        self,
    ):
        other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0798765432",
        )

        response = self.client.get(
            reverse(
                "business-payment-detail",
                kwargs={
                    "business_id": other_business.id,
                    "payment_id": self.payment.id,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_retrieve_payment(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(self.url)

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
