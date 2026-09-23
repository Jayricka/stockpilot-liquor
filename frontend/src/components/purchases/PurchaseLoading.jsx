function PurchaseLoading({
  loading,
  hasPurchases,
  searching,
}) {
  if (loading) {
    return (
      <div className="purchases-empty">
        <h3>Loading purchases...</h3>

        <p>
          Fetching your purchase records.
        </p>
      </div>
    )
  }

  if (!hasPurchases) {
    return (
      <div className="purchases-empty">
        <h3>No purchases found</h3>

        <p>
          {searching
            ? 'Try another search.'
            : 'Create a purchase to record incoming stock.'}
        </p>
      </div>
    )
  }

  return null
}

export default PurchaseLoading
