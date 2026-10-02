from django.db import transaction

from ..models import Payment
from .payments import PaymentService


class MpesaCallbackService:

    @staticmethod
    def _get_callback_data(payload):
        try:
            callback = payload["Body"]["stkCallback"]
        except (KeyError, TypeError):
            raise ValueError(
                "Invalid M-Pesa callback payload."
            )

        if not isinstance(callback, dict):
            raise ValueError(
                "Invalid M-Pesa callback payload."
            )

        return callback

    @staticmethod
    def _get_required_value(
        callback,
        field_name,
        error_message,
    ):
        value = callback.get(field_name)

        if value is None:
            raise ValueError(error_message)

        return value

    @staticmethod
    def _get_metadata(callback):
        metadata = callback.get(
            "CallbackMetadata",
            {},
        )

        items = metadata.get("Item", [])

        if not isinstance(items, list):
            return {}

        return {
            item.get("Name"): item.get("Value")
            for item in items
            if isinstance(item, dict)
            and item.get("Name")
        }

    @staticmethod
    @transaction.atomic
    def process_callback(payload):
        callback = MpesaCallbackService._get_callback_data(
            payload
        )

        checkout_request_id = (
            MpesaCallbackService._get_required_value(
                callback,
                "CheckoutRequestID",
                "CheckoutRequestID is required.",
            )
        )

        result_code = (
            MpesaCallbackService._get_required_value(
                callback,
                "ResultCode",
                "ResultCode is required.",
            )
        )

        payment = (
            Payment.objects.select_for_update()
            .filter(
                checkout_request_id=checkout_request_id,
            )
            .first()
        )

        if payment is None:
            return None

        if payment.status != Payment.Status.PENDING:
            return payment

        result_description = callback.get(
            "ResultDesc",
            "",
        )

        if result_code == 0:
            metadata = (
                MpesaCallbackService._get_metadata(
                    callback
                )
            )

            mpesa_receipt = metadata.get(
                "MpesaReceiptNumber"
            )

            if not mpesa_receipt:
                raise ValueError(
                    "M-Pesa receipt is required for "
                    "successful payments."
                )

            return PaymentService.mark_success(
                payment=payment,
                mpesa_receipt=mpesa_receipt,
                result_code=result_code,
                result_description=result_description,
            )

        return PaymentService.mark_failed(
            payment=payment,
            result_code=result_code,
            result_description=result_description,
        )
