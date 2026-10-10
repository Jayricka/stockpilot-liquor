
import { useState } from 'react'

function PaymentForm({
  defaultAmount,
  currency = 'KES',
  loading,
  error,
  payment,
  onSubmit,
}) {
  const [phoneNumber, setPhoneNumber] =
    useState('')

  const handleSubmit = async (event) => {
    event.preventDefault()

    await onSubmit({
      phoneNumber: phoneNumber.trim(),
    })
  }

  const paymentPending =
    payment?.status === 'PENDING'

  return (
    <section className="billing-card">
      <div className="billing-card-header">
        <div>
          <p className="billing-label">
            M-Pesa payment
          </p>

          <h2>Make a payment</h2>
        </div>

        {paymentPending && (
          <span className="billing-status">
            Pending
          </span>
        )}
      </div>

      <form
        className="billing-payment-form"
        onSubmit={handleSubmit}
      >
        <label>
          <span>Amount due</span>

          <input
            type="text"
            value={
              defaultAmount == null
                ? 'Unavailable'
                : `${currency} ${Number(
                    defaultAmount,
                  ).toLocaleString()}`
            }
            readOnly
            aria-readonly="true"
          />
        </label>

        <label>
          <span>M-Pesa phone number</span>

          <input
            type="tel"
            name="phone_number"
            autoComplete="tel"
            inputMode="tel"
            placeholder="0712345678"
            value={phoneNumber}
            onChange={(event) =>
              setPhoneNumber(event.target.value)
            }
            required
          />
        </label>

        {error && (
          <div
            className="billing-error"
            role="alert"
          >
            {error}
          </div>
        )}

        {paymentPending && (
          <div className="billing-trial">
            <strong>STK Push sent</strong>

            <span>
              Check your phone and enter your
              M-Pesa PIN to complete the payment.
            </span>
          </div>
        )}

        {payment?.status === 'FAILED' && (
          <div className="billing-error" role="status">
            The payment was not completed. You can
            try again.
          </div>
        )}

        <button
          type="submit"
          className="billing-plan-action"
          disabled={
            loading ||
            defaultAmount == null ||
            paymentPending
          }
        >
          {loading
            ? 'Sending STK Push...'
            : paymentPending
              ? 'Payment pending'
              : 'Pay with M-Pesa'}
        </button>
      </form>
    </section>
  )
}

export default PaymentForm
