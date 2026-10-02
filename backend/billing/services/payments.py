from django.db import transaction
from django.utils import timezone

from ..models import Payment
from .mpesa import MpesaGateway


class PaymentService:

    @staticmethod
    @transaction.atomic
    def create_payment(
        subscription,
        amount,
        phone_number,
        currency="KES",
    ):
        return Payment.objects.create(
            subscription=subscription,
            amount=amount,
            currency=currency,
            phone_number=phone_number,
            status=Payment.Status.PENDING,
        )

    @staticmethod
    @transaction.atomic
    def initiate_mpesa_payment(
        payment,
        gateway=None,
    ):
        if payment.status != Payment.Status.PENDING:
            raise ValueError(
                "Only pending payments can be initiated."
            )

        if gateway is None:
            gateway = MpesaGateway()

        result = gateway.stk_push(payment)

        payment.merchant_request_id = (
            result["merchant_request_id"]
        )
        payment.checkout_request_id = (
            result["checkout_request_id"]
        )

        payment.save(
            update_fields=[
                "merchant_request_id",
                "checkout_request_id",
            ]
        )

        return payment

    @staticmethod
    @transaction.atomic
    def mark_success(
        payment,
        mpesa_receipt="",
        result_code=None,
        result_description="",
    ):
        if payment.status != Payment.Status.PENDING:
            raise ValueError(
                "Only pending payments can be marked "
                "successful."
            )

        payment.status = Payment.Status.SUCCESS
        payment.mpesa_receipt = mpesa_receipt
        payment.result_code = result_code
        payment.result_description = result_description
        payment.completed_at = timezone.now()

        payment.save(
            update_fields=[
                "status",
                "mpesa_receipt",
                "result_code",
                "result_description",
                "completed_at",
            ]
        )

        return payment

    @staticmethod
    @transaction.atomic
    def mark_failed(
        payment,
        result_code=None,
        result_description="",
    ):
        if payment.status != Payment.Status.PENDING:
            raise ValueError(
                "Only pending payments can be marked "
                "failed."
            )

        payment.status = Payment.Status.FAILED
        payment.result_code = result_code
        payment.result_description = result_description
        payment.completed_at = timezone.now()

        payment.save(
            update_fields=[
                "status",
                "result_code",
                "result_description",
                "completed_at",
            ]
        )

        return payment

    @staticmethod
    @transaction.atomic
    def cancel(payment):
        if payment.status != Payment.Status.PENDING:
            raise ValueError(
                "Only pending payments can be cancelled."
            )

        payment.status = Payment.Status.CANCELLED
        payment.completed_at = timezone.now()

        payment.save(
            update_fields=[
                "status",
                "completed_at",
            ]
        )

        return payment

    @staticmethod
    @transaction.atomic
    def expire(payment):
        if payment.status != Payment.Status.PENDING:
            raise ValueError(
                "Only pending payments can be expired."
            )

        payment.status = Payment.Status.EXPIRED
        payment.completed_at = timezone.now()

        payment.save(
            update_fields=[
                "status",
                "completed_at",
            ]
        )

        return payment
