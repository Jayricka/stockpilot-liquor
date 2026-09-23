import DeliveryStatus from './DeliveryStatus'

function DeliveryTable({
  deliveries,
  members,
  actionLoading,
  onAssign,
  onStart,
  onComplete,
  onCancel,
}) {
  function getActions(delivery) {
    if (delivery.status === 'PENDING') {
      return (
        <select
          value=""
          onChange={(event) =>
            onAssign(
              delivery,
              event.target.value,
            )
          }
          disabled={actionLoading}
          aria-label={`Assign ${delivery.customer_name}`}
        >
          <option value="">
            Assign
          </option>

          {members.map((member) => (
            <option
              key={member.user_id}
              value={member.user_id}
            >
              {member.full_name ||
                member.email}
            </option>
          ))}
        </select>
      )
    }

    if (
      delivery.status === 'ASSIGNED'
    ) {
      return (
        <button
          type="button"
          onClick={() => onStart(delivery)}
          disabled={actionLoading}
        >
          Start
        </button>
      )
    }

    if (
      delivery.status ===
      'OUT_FOR_DELIVERY'
    ) {
      return (
        <button
          type="button"
          onClick={() =>
            onComplete(delivery)
          }
          disabled={actionLoading}
        >
          Complete
        </button>
      )
    }

    return null
  }

  return (
    <div className="deliveries-table-wrap">
      <table className="deliveries-table">
        <thead>
          <tr>
            <th>Customer</th>
            <th>Invoice</th>
            <th>Contact</th>
            <th>Address</th>
            <th>Fee</th>
            <th>Assigned To</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>

        <tbody>
          {deliveries.map((delivery) => (
            <tr key={delivery.id}>
              <td>
                <strong>
                  {delivery.customer_name}
                </strong>

                {delivery.notes && (
                  <small>
                    {delivery.notes}
                  </small>
                )}
              </td>

              <td>
                {delivery.invoice_number ||
                  '—'}
              </td>

              <td>
                {delivery.customer_phone}
              </td>

              <td>
                {delivery.delivery_address}
              </td>

              <td>
                KES{' '}
                {Number(
                  delivery.delivery_fee || 0,
                ).toLocaleString()}
              </td>

              <td>
                {delivery.assigned_to_name ||
                  'Unassigned'}
              </td>

              <td>
                <DeliveryStatus
                  status={delivery.status}
                />
              </td>

              <td>
                <div className="delivery-row-actions">
                  {getActions(delivery)}

                  {delivery.status !==
                    'DELIVERED' &&
                    delivery.status !==
                      'CANCELLED' && (
                      <button
                        type="button"
                        className="danger"
                        onClick={() =>
                          onCancel(delivery)
                        }
                        disabled={
                          actionLoading
                        }
                      >
                        Cancel
                      </button>
                    )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default DeliveryTable
