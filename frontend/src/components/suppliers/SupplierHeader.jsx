function SupplierHeader({
  businesses,
  businessId,
  onBusinessChange,
  onAdd,
}) {
  return (
    <header className="suppliers-header">
      <div>
        <span className="suppliers-eyebrow">
          PROCUREMENT
        </span>

        <h1>Suppliers</h1>

        <p>
          Manage the suppliers that support
          your inventory.
        </p>
      </div>

      <div className="suppliers-actions">
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
          + Add Supplier
        </button>
      </div>
    </header>
  )
}

export default SupplierHeader
