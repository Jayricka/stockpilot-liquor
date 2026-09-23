function DeliveryLoading({
  loading,
  hasDeliveries,
  searching,
}) {
  if (loading) {
    return (
      <div className="deliveries-empty">
        <h3>Loading deliveries...</h3>

        <p>
          Fetching your delivery records.
        </p>
      </div>
    )
  }

  if (!hasDeliveries) {
    return (
      <div className="deliveries-empty">
        <h3>No deliveries found</h3>

        <p>
          {searching
            ? 'Try another search.'
            : 'Completed sales can be converted into deliveries.'}
        </p>
      </div>
    )
  }

  return null
}

export default DeliveryLoading
