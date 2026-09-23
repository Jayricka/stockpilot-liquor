function PurchaseHeader({
  businesses,
  businessId,
  onBusinessChange,
  onAdd,
}) {
  return (
    <header className="purchases-header">
      <div>
        <span className="purchases-eyebrow">
          PROCUREMENT
        </span>

        <h1>Purchases</h1>

        <p>
          Manage supplier purchases and incoming stock.
        </p>
      </div>

      <div className="purchases-actions">
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
          + New Purchase
        </button>
      </div>
    </header>
  )
}

export default PurchaseHeader
