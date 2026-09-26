function ProductLoading() {
  return (
    <div className="product-loading" aria-label="Loading products">
      <div className="product-loading-header">
        <div className="product-skeleton product-skeleton-title" />
        <div className="product-skeleton product-skeleton-button" />
      </div>

      <div className="product-loading-stats">
        {[1, 2, 3, 4].map((item) => (
          <div
            key={item}
            className="product-skeleton-card"
          >
            <div className="product-skeleton product-skeleton-icon" />
            <div className="product-skeleton product-skeleton-label" />
            <div className="product-skeleton product-skeleton-value" />
          </div>
        ))}
      </div>

      <div className="product-loading-table">
        <div className="product-skeleton product-skeleton-table-header" />

        {[1, 2, 3, 4, 5].map((item) => (
          <div
            key={item}
            className="product-skeleton-row"
          >
            <div className="product-skeleton" />
            <div className="product-skeleton" />
            <div className="product-skeleton" />
            <div className="product-skeleton" />
            <div className="product-skeleton" />
          </div>
        ))}
      </div>
    </div>
  )
}

export default ProductLoading
