function DeliveryStatus({ status }) {
  const labels = {
    PENDING: 'Pending',
    ASSIGNED: 'Assigned',
    OUT_FOR_DELIVERY: 'Out for Delivery',
    DELIVERED: 'Delivered',
    CANCELLED: 'Cancelled',
  }

  return (
    <span
      className={`delivery-status delivery-status-${status
        ?.toLowerCase()
        .replaceAll('_', '-')}`}
    >
      {labels[status] || status}
    </span>
  )
}

export default DeliveryStatus
