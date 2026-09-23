function DeliveryFilters({
  count,
  search,
  status,
  onSearch,
  onStatusChange,
}) {
  return (
    <div className="deliveries-toolbar">
      <strong>
        {count} delivery
        {count !== 1 ? 'ies' : 'y'}
      </strong>

      <div className="delivery-filters">
        <input
          type="search"
          value={search}
          onChange={onSearch}
          placeholder="Search customer or invoice..."
          aria-label="Search deliveries"
        />

        <select
          value={status}
          onChange={onStatusChange}
          aria-label="Filter by delivery status"
        >
          <option value="">All statuses</option>
          <option value="PENDING">Pending</option>
          <option value="ASSIGNED">Assigned</option>
          <option value="OUT_FOR_DELIVERY">
            Out for Delivery
          </option>
          <option value="DELIVERED">
            Delivered
          </option>
          <option value="CANCELLED">
            Cancelled
          </option>
        </select>
      </div>
    </div>
  )
}

export default DeliveryFilters
