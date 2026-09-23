function SupplierFilters({
  count,
  search,
  onSearch,
}) {
  return (
    <div className="suppliers-toolbar">
      <strong>
        {count} supplier
        {count !== 1 ? 's' : ''}
      </strong>

      <input
        type="search"
        value={search}
        onChange={onSearch}
        placeholder="Search suppliers..."
        aria-label="Search suppliers"
      />
    </div>
  )
}

export default SupplierFilters
