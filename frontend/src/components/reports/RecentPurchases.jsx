function RecentPurchases({
  purchases,
}) {
  return (
    <article className="report-panel">
      <div className="report-panel-header">
        <div>
          <span>PROCUREMENT</span>
          <h2>Recent purchases</h2>
        </div>
      </div>

      {!purchases.length ? (
        <p className="report-empty">
          No completed purchases yet.
        </p>
      ) : (
        <div className="report-table-wrap">
          <table className="report-table">
            <thead>
              <tr>
                <th>Reference</th>
                <th>Supplier</th>
                <th>Date</th>
                <th>Total</th>
              </tr>
            </thead>

            <tbody>
              {purchases.map((purchase) => (
                <tr key={purchase.id}>
                  <td>
                    <strong>
                      {purchase.reference_number}
                    </strong>
                  </td>

                  <td>
                    {purchase.supplier__name ||
                      '—'}
                  </td>

                  <td>
                    {purchase.purchase_date}
                  </td>

                  <td>
                    KES{' '}
                    {Number(
                      purchase.total_amount || 0,
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

export default RecentPurchases
