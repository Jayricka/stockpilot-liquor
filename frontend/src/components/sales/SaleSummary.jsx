function SaleSummary({
  subtotal,
  discount,
  onDiscountChange,
  total,
  paymentMethod,
  onPaymentMethodChange,
  amountReceived,
  onAmountReceivedChange,
  change,
  onComplete,
  loading,
}) {
  const cashAmount =
    Number(amountReceived || 0)

  const insufficientCash =
    paymentMethod === 'CASH' &&
    cashAmount < total

  return (
    <section className="sale-summary">
      <div className="sale-section-header">
        <div>
          <span>Checkout</span>
          <h2>Sale summary</h2>
        </div>
      </div>

      <div className="sale-summary-lines">
        <div>
          <span>Subtotal</span>

          <strong>
            KES{' '}
            {Number(
              subtotal,
            ).toLocaleString()}
          </strong>
        </div>

        <label className="sale-discount">
          <span>Discount</span>

          <div>
            <span>KES</span>

            <input
              type="number"
              min="0"
              step="0.01"
              value={discount}
              onChange={(event) =>
                onDiscountChange(
                  event.target.value,
                )
              }
              placeholder="0.00"
            />
          </div>
        </label>

        <div className="sale-total">
          <span>Total</span>

          <strong>
            KES{' '}
            {Number(
              total,
            ).toLocaleString()}
          </strong>
        </div>
      </div>

      <div className="sale-payment">
        <span className="sale-field-label">
          Payment method
        </span>

        <div className="payment-methods">
          {[
            ['CASH', 'Cash'],
            ['MPESA', 'M-Pesa'],
            ['CARD', 'Card'],
            ['CREDIT', 'Credit'],
          ].map(
            ([value, label]) => (
              <button
                key={value}
                type="button"
                className={
                  paymentMethod === value
                    ? 'payment-method active'
                    : 'payment-method'
                }
                onClick={() =>
                  onPaymentMethodChange(
                    value,
                  )
                }
              >
                {label}
              </button>
            ),
          )}
        </div>
      </div>

      {paymentMethod === 'CASH' && (
        <div className="cash-payment">
          <label>
            <span>
              Amount received
            </span>

            <div className="cash-input">
              <span>KES</span>

              <input
                type="number"
                min="0"
                step="0.01"
                value={
                  amountReceived
                }
                onChange={(event) =>
                  onAmountReceivedChange(
                    event.target.value,
                  )
                }
                placeholder="0.00"
              />
            </div>
          </label>

          <div className="change-row">
            <span>Change</span>

            <strong>
              KES{' '}
              {Number(
                change,
              ).toLocaleString()}
            </strong>
          </div>

          {insufficientCash && (
            <p className="payment-warning">
              Amount received is less than
              the sale total.
            </p>
          )}
        </div>
      )}

      <button
        type="button"
        className="sale-complete-button"
        disabled={
          loading ||
          !total ||
          insufficientCash
        }
        onClick={onComplete}
      >
        {loading
          ? 'Completing sale...'
          : 'Complete Sale'}
      </button>
    </section>
  )
}

export default SaleSummary
