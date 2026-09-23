function RecentSales({ sales }) {
  return (
    <article className="report-panel">
      <div className="report-panel-header">
        <div>
          <span>SALES</span>
          <h2>Recent sales</h2>
        </div>
      </div>

      {!sales.length ? (
        <p className="report-empty">
          No completed sales yet.
        </p>
      ) : (
        <div className="report-table-wrap">
          <table className="report-table">
            <thead>
              <tr>
                <th>Invoice</th>
                <th>Date</th>
                <th>Payment</th>
                <th>Total</th>
                <th>Profit</th>
              </tr>
            </thead>

            <tbody>
              {sales.map((sale) => (
                <tr key={sale.id}>
                  <td>
                    <strong>
                      {sale.invoice_number}
                    </strong>
                  </td>

                  <td>{sale.sale_date}</td>

                  <td>
                    {sale.payment_method}
                  </td>

                  <td>
                    KES{' '}
                    {Number(
                      sale.total_amount || 0,
                    ).toLocaleString()}
                  </td>

                  <td className="report-profit">
                    KES{' '}
                    {Number(
                      sale.gross_profit || 0,
                    ).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </article>
  )
}

export default RecentSales
