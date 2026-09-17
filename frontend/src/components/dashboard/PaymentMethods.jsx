function formatMethod(value) {
  return value
    ?.replaceAll('_', ' ')
    .replace(/\b\w/g, (letter) =>
      letter.toUpperCase(),
    )
}

function PaymentMethods({ payments = [] }) {
  const total = payments.reduce(
    (sum, item) => sum + Number(item.total || 0),
    0,
  )

  return (
    <article className="dashboard-card">
      <div className="card-heading">
        <div>
          <span>Sales mix</span>
          <h2>Payment methods</h2>
        </div>
      </div>

      <div className="payment-list">
        {payments.length ? (
          payments.map((item) => {
            const percentage = total
              ? (Number(item.total) / total) * 100
              : 0

            return (
              <div className="payment-row" key={item.payment_method}>
                <div>
                  <strong>
                    {formatMethod(item.payment_method)}
                  </strong>
                  <span>{item.count} sales</span>
                </div>

                <div className="payment-value">
                  <strong>
                    KES {Number(item.total).toLocaleString()}
                  </strong>

                  <div className="payment-bar">
                    <span
                      style={{ width: `${percentage}%` }}
                    />
                  </div>
                </div>
              </div>
            )
          })
        ) : (
          <p className="empty-message">
            No sales recorded today.
          </p>
        )}
      </div>
    </article>
  )
}

export default PaymentMethods
