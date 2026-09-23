function SupplierLoading({
  loading,
  hasSuppliers,
  searching,
}) {
  if (loading) {
    return (
      <div className="suppliers-empty">
        <h3>Loading suppliers...</h3>

        <p>
          Fetching your supplier records.
        </p>
      </div>
    )
  }

  if (!hasSuppliers) {
    return (
      <div className="suppliers-empty">
        <h3>No suppliers found</h3>

        <p>
          {searching
            ? 'Try another search.'
            : 'Add your first supplier to get started.'}
        </p>
      </div>
    )
  }

  return null
}

export default SupplierLoading
