function PurchaseStatus({ status }) {
  const labels = {
    DRAFT: 'Draft',
    COMPLETED: 'Completed',
    CANCELLED: 'Cancelled',
  }

  return (
    <span
      className={`purchase-status purchase-status-${status
        ?.toLowerCase()
        .replaceAll('_', '-')}`}
    >
      {labels[status] || status}
    </span>
  )
}

export default PurchaseStatus
