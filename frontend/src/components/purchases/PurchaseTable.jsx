import PurchaseStatus from './PurchaseStatus'

function PurchaseTable({
  purchases,
  actionLoading,
  onComplete,
  onCancel,
}) {
  function getActions(purchase) {
    if (purchase.status === 'DRAFT') {
      return (
        <>
          <button
            type="button"
            onClick={() => onComplete(purchase)}
            disabled={actionLoading}
          >
            Receive Stock
          </button>

          <button
            type="button"
            className="danger"
            onClick={() => onCancel(purchase)}
            disabled={actionLoading}
          >
            Cancel
          </button>
        </>
      )
    }

    return null
  }

  return (
    <div className="purchases-table-wrap">
      <table className="purchases-table">
        <thead>
          <tr>
            <th>Reference</th>
            <th>Supplier</th>
            <th>Date</th>
            <th>Items</th>
            <th>Total</th>
            <th>Created By</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {purchases.map((purchase) => (
            <tr key={purchase.id}>
              <td>
                <strong>
                  {purchase.reference_number}
                </strong>

                {purchase.notes && (
                  <small>
                    {purchase.notes}
                  </small>
                )}
              </td>

              <td>
                {purchase.supplier_name || '—'}
              </td>

              <td>
                {purchase.purchase_date}
              </td>

              <td>
                {purchase.items?.length || 0}
              </td>

              <td>
                KES{' '}
                {Number(
                  purchase.total_amount || 0,
                ).toLocaleString()}
              </td>

              <td>
                {purchase.created_by_name || '—'}
              </td>

              <td>
                <PurchaseStatus
                  status={purchase.status}
                />
              </td>

              <td>
                <div className="purchase-row-actions">
                  {getActions(purchase)}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default PurchaseTable
