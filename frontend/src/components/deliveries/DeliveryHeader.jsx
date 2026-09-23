function DeliveryHeader({
  businesses,
  businessId,
  onBusinessChange,
  onAdd,
}) {
  return (
    <header className="deliveries-header">
      <div>
        <span className="deliveries-eyebrow">
          LOGISTICS
        </span>

        <h1>Deliveries</h1>

        <p>
          Track and manage customer deliveries.
        </p>
      </div>

      <div className="deliveries-actions">
        <select
          value={businessId}
          onChange={onBusinessChange}
          aria-label="Select business"
        >
          {!businesses.length && (
            <option value="">
              No businesses
            </option>
          )}

          {businesses.map((business) => (
            <option
              key={business.id}
              value={business.id}
            >
              {business.name}
            </option>
          ))}
        </select>

        <button
          type="button"
          onClick={onAdd}
          disabled={!businessId}
        >
          + New Delivery
        </button>
      </div>
    </header>
  )
}

export default DeliveryHeader
