function RecentSales({ sales = [] }) {
  return (
    <article className="dashboard-card">
      <div className="card-heading">
        <div>
          <span>Latest activity</span>
          <h2>Recent sales</h2>
        </div>
      </div>

      <div className="sales-list">
        {sales.length ? (
          sales.map((sale) => (
            <div className="sale-row" key={sale.id}>
              <div>
                <strong>{sale.invoice_number}</strong>
                <span>{sale.payment_method}</span>
              </div>

              <div>
                <strong>
                  KES {Number(sale.total_amount).toLocaleString()}
                </strong>

                <span className="profit">
                  +KES {Number(sale.gross_profit).toLocaleString()}
                </span>
              </div>
            </div>
          ))
        ) : (
          <p className="empty-message">
            No completed sales yet.
          </p>
        )}
      </div>
    </article>
  )
}

export default RecentSales
