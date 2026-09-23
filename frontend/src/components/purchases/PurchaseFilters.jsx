function PurchaseFilters({
  count,
  search,
  status,
  onSearch,
  onStatusChange,
}) {
  return (
    <div className="purchases-toolbar">
      <strong>
        {count} purchase
        {count !== 1 ? 's' : ''}
      </strong>

      <div className="purchase-filters">
        <input
          type="search"
          value={search}
          onChange={onSearch}
          placeholder="Search reference or supplier..."
          aria-label="Search purchases"
        />

        <select
          value={status}
          onChange={onStatusChange}
          aria-label="Filter by purchase status"
        >
          <option value="">
            All statuses
          </option>

          <option value="DRAFT">
            Draft
          </option>

          <option value="COMPLETED">
            Completed
          </option>

          <option value="CANCELLED">
            Cancelled
          </option>
        </select>
      </div>
    </div>
  )
}

export default PurchaseFilters
