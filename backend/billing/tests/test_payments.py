from unittest.mock import Mock, patch

from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase

from billing.models import Payment, Plan, Subscription
from billing.services.payments import PaymentService
from businesses.models import Business


class PaymentServiceTestCase(APITestCase):

    def setUp(self):
        self.business = Business.objects.create(
            name="Test Liquor Store",
            business_type="liquor_store",
            phone="0712345678",
        )

        self.plan = Plan.objects.get(
            code=Plan.Code.STARTER,
        )

        now = timezone.now()

        self.subscription = Subscription.objects.create(
            business=self.business,
            plan=self.plan,
            status=Subscription.Status.ACTIVE,
            trial_started_at=now - timedelta(days=7),
            trial_ends_at=now - timedelta(days=1),
        )

    def create_payment(self):
        return PaymentService.create_payment(
            subscription=self.subscription,
            amount=1500,
            phone_number="0712345678",
        )

    def test_create_payment(self):
        payment = self.create_payment()

        self.assertEqual(
            payment.subscription,
            self.subscription,
        )
        self.assertEqual(payment.amount, 1500)
        self.assertEqual(payment.currency, "KES")
        self.assertEqual(
            payment.phone_number,
            "0712345678",
        )
        self.assertEqual(
            payment.status,
            Payment.Status.PENDING,
        )
        self.assertIsNone(payment.completed_at)

    def test_create_payment_supports_custom_currency(self):
        payment = PaymentService.create_payment(
            subscription=self.subscription,
            amount=2000,
            phone_number="0712345678",
            currency="USD",
        )

        self.assertEqual(payment.currency, "USD")

    @patch(
        "billing.services.payments.MpesaGateway"
    )
    def test_initiate_mpesa_payment(
        self,
        mock_gateway_class,
    ):
        payment = self.create_payment()

        gateway = Mock()

        gateway.stk_push.return_value = {
            "merchant_request_id": "merchant-123",
            "checkout_request_id": "checkout-123",
        }

        mock_gateway_class.return_value = gateway

        result = PaymentService.initiate_mpesa_payment(
            payment
        )

        result.refresh_from_db()

        self.assertEqual(
            result.merchant_request_id,
            "merchant-123",
        )
        self.assertEqual(
            result.checkout_request_id,
            "checkout-123",
        )
        self.assertEqual(
            result.status,
            Payment.Status.PENDING,
        )

        gateway.stk_push.assert_called_once_with(
            payment
        )

    def test_initiate_mpesa_payment_requires_pending(
        self,
    ):
        payment = self.create_payment()

        PaymentService.mark_success(payment)

        with self.assertRaisesMessage(
            ValueError,
            "Only pending payments can be initiated.",
        ):
            PaymentService.initiate_mpesa_payment(
                payment
            )

    def test_initiate_mpesa_payment_accepts_gateway(
        self,
    ):
        payment = self.create_payment()

        gateway = Mock()

        gateway.stk_push.return_value = {
            "merchant_request_id": "merchant-456",
            "checkout_request_id": "checkout-456",
        }

        result = PaymentService.initiate_mpesa_payment(
            payment,
            gateway=gateway,
        )

        result.refresh_from_db()

        self.assertEqual(
            result.merchant_request_id,
            "merchant-456",
        )
        self.assertEqual(
            result.checkout_request_id,
            "checkout-456",
        )

        gateway.stk_push.assert_called_once_with(
            payment
        )

    def test_mark_success(self):
        payment = self.create_payment()

        result = PaymentService.mark_success(
            payment,
            mpesa_receipt="QWE123456",
            result_code=0,
            result_description="Success",
        )

        self.assertEqual(
            result.status,
            Payment.Status.SUCCESS,
        )
        self.assertEqual(
            result.mpesa_receipt,
            "QWE123456",
        )
        self.assertEqual(result.result_code, 0)
        self.assertEqual(
            result.result_description,
            "Success",
        )
        self.assertIsNotNone(result.completed_at)

    def test_mark_failed(self):
        payment = self.create_payment()

        result = PaymentService.mark_failed(
            payment,
            result_code=1,
            result_description="Payment failed",
        )

        self.assertEqual(
            result.status,
            Payment.Status.FAILED,
        )
        self.assertEqual(result.result_code, 1)
        self.assertEqual(
            result.result_description,
            "Payment failed",
        )
        self.assertIsNotNone(result.completed_at)

    def test_cancel(self):
        payment = self.create_payment()

        result = PaymentService.cancel(payment)

        self.assertEqual(
            result.status,
            Payment.Status.CANCELLED,
        )
        self.assertIsNotNone(result.completed_at)

    def test_expire(self):
        payment = self.create_payment()

        result = PaymentService.expire(payment)

        self.assertEqual(
            result.status,
            Payment.Status.EXPIRED,
        )
        self.assertIsNotNone(result.completed_at)

    def test_success_requires_pending_payment(self):
        payment = self.create_payment()
        PaymentService.mark_success(payment)

        with self.assertRaisesMessage(
            ValueError,
            "Only pending payments can be marked successful.",
        ):
            PaymentService.mark_success(payment)

    def test_failed_requires_pending_payment(self):
        payment = self.create_payment()
        PaymentService.mark_failed(payment)

        with self.assertRaisesMessage(
            ValueError,
            "Only pending payments can be marked failed.",
        ):
            PaymentService.mark_failed(payment)

    def test_cancel_requires_pending_payment(self):
        payment = self.create_payment()
        PaymentService.cancel(payment)

        with self.assertRaisesMessage(
            ValueError,
            "Only pending payments can be cancelled.",
        ):
            PaymentService.cancel(payment)

    def test_expire_requires_pending_payment(self):
        payment = self.create_payment()
        PaymentService.expire(payment)

        with self.assertRaisesMessage(
            ValueError,
            "Only pending payments can be expired.",
        ):
            PaymentService.expire(payment)
