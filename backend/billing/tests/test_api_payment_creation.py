from datetime import timedelta
from unittest.mock import patch

from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from billing.models import Payment, Plan, Subscription
from billing.services.mpesa import MpesaGatewayError
from businesses.models import Business, BusinessMembership


class BillingAPITestBase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="owner@example.com",
            password="StrongPassword123",
            first_name="John",
            last_name="Owner",
        )

        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        BusinessMembership.objects.create(
            user=self.user,
            business=self.business,
            role=BusinessMembership.Role.OWNER,
            is_active=True,
        )

        self.plan = Plan.objects.get(
            code=Plan.Code.STARTER,
            is_active=True,
        )

        now = timezone.now()

        self.subscription = Subscription.objects.create(
            business=self.business,
            plan=self.plan,
            status=Subscription.Status.TRIALING,
            trial_started_at=now,
            trial_ends_at=now + timedelta(days=7),
        )

        self.client.force_authenticate(
            user=self.user,
        )

    def payment_url(self):
        return (
            f"/api/businesses/"
            f"{self.business.id}/payments/"
        )


class PaymentCreationAPITestCase(BillingAPITestBase):

    @patch("billing.services.payments.MpesaGateway")
    def test_member_can_create_payment(
        self,
        gateway_class,
    ):
        gateway = gateway_class.return_value

        gateway.stk_push.return_value = {
            "merchant_request_id": "merchant-123",
            "checkout_request_id": "checkout-123",
        }

        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        payment = Payment.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            payment.subscription,
            self.subscription,
        )

    @patch("billing.services.payments.MpesaGateway")
    def test_payment_amount_uses_subscription_plan_price(
        self,
        gateway_class,
    ):
        gateway = gateway_class.return_value

        gateway.stk_push.return_value = {
            "merchant_request_id": "merchant-123",
            "checkout_request_id": "checkout-123",
        }

        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        payment = Payment.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            payment.amount,
            self.subscription.plan.price,
        )

        self.assertEqual(
            payment.currency,
            self.subscription.plan.currency,
        )

    @patch("billing.services.payments.MpesaGateway")
    def test_payment_creation_ignores_client_amount(
        self,
        gateway_class,
    ):
        gateway = gateway_class.return_value

        gateway.stk_push.return_value = {
            "merchant_request_id": "merchant-123",
            "checkout_request_id": "checkout-123",
        }

        response = self.client.post(
            self.payment_url(),
            {
                "amount": 999,
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        payment = Payment.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            payment.amount,
            self.subscription.plan.price,
        )

        self.assertEqual(
            payment.currency,
            self.subscription.plan.currency,
        )

        gateway.stk_push.assert_called_once_with(
            payment,
        )

    def test_blank_phone_number_is_rejected(self):
        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "   ",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_missing_phone_number_is_rejected(self):
        response = self.client.post(
            self.payment_url(),
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cancelled_subscription_cannot_create_payment(self):
        self.subscription.status = (
            Subscription.Status.CANCELLED
        )
        self.subscription.save(
            update_fields=["status"],
        )

        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            response.data["detail"],
            "Payments cannot be created for this subscription.",
        )

    def test_expired_subscription_cannot_create_payment(self):
        self.subscription.status = (
            Subscription.Status.EXPIRED
        )
        self.subscription.save(
            update_fields=["status"],
        )

        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertEqual(
            response.data["detail"],
            "Payments cannot be created for this subscription.",
        )

    def test_other_business_cannot_create_payment(self):
        other_business = Business.objects.create(
            name="Other Liquor Store",
            business_type="liquor_store",
            phone="0798765432",
        )

        url = (
            f"/api/businesses/"
            f"{other_business.id}/payments/"
        )

        response = self.client.post(
            url,
            {
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_create_payment(self):
        self.client.force_authenticate(
            user=None,
        )

        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch("billing.services.payments.MpesaGateway")
    def test_mpesa_failure_returns_bad_gateway(
        self,
        gateway_class,
    ):
        gateway = gateway_class.return_value

        gateway.stk_push.side_effect = MpesaGatewayError(
            "M-Pesa gateway unavailable.",
        )

        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_502_BAD_GATEWAY,
        )

    @patch("billing.services.payments.MpesaGateway")
    def test_client_cannot_inject_payment_status(
        self,
        gateway_class,
    ):
        gateway = gateway_class.return_value

        gateway.stk_push.return_value = {
            "merchant_request_id": "merchant-123",
            "checkout_request_id": "checkout-123",
        }

        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "0712345678",
                "status": "SUCCESS",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        payment = Payment.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            payment.status,
            Payment.Status.PENDING,
        )

    @patch("billing.services.payments.MpesaGateway")
    def test_client_cannot_inject_mpesa_receipt(
        self,
        gateway_class,
    ):
        gateway = gateway_class.return_value

        gateway.stk_push.return_value = {
            "merchant_request_id": "merchant-123",
            "checkout_request_id": "checkout-123",
        }

        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "0712345678",
                "mpesa_receipt": "FAKE123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        payment = Payment.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            payment.mpesa_receipt,
            "",
        )

    @patch("billing.services.payments.MpesaGateway")
    def test_payment_preserves_subscription(
        self,
        gateway_class,
    ):
        gateway = gateway_class.return_value

        gateway.stk_push.return_value = {
            "merchant_request_id": "merchant-123",
            "checkout_request_id": "checkout-123",
        }

        response = self.client.post(
            self.payment_url(),
            {
                "phone_number": "0712345678",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        payment = Payment.objects.get(
            id=response.data["id"],
        )

        self.assertEqual(
            payment.subscription_id,
            self.subscription.id,
        )
