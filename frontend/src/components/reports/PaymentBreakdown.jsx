function PaymentBreakdown({
  payments,
}) {
  const total = payments.reduce(
    (sum, payment) =>
      sum + Number(payment.total || 0),
    0,
  )

  return (
    <article className="report-panel">
      <div className="report-panel-header">
        <div>
          <span>PAYMENTS</span>
          <h2>Sales by payment method</h2>
        </div>

        <strong>
          KES {total.toLocaleString()}
        </strong>
      </div>

      {!payments.length ? (
        <p className="report-empty">
          No sales recorded today.
        </p>
      ) : (
        <div className="payment-list">
          {payments.map((payment) => {
            const amount =
              Number(payment.total || 0)

            const percentage = total
              ? (amount / total) * 100
              : 0

            return (
              <div
                className="payment-row"
                key={payment.payment_method}
              >
                <div>
                  <strong>
                    {payment.payment_method}
                  </strong>

                  <span>
                    {payment.count} sale
                    {payment.count !== 1
                      ? 's'
                      : ''}
                  </span>
                </div>

                <div className="payment-value">
                  <strong>
                    KES {amount.toLocaleString()}
                  </strong>

                  <span>
                    {percentage.toFixed(0)}%
                  </span>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </article>
  )
}

export default PaymentBreakdown
