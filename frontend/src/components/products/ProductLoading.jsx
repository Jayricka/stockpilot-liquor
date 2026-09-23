function ProductLoading() {
  return (
    <section className="sp-product-loading">
      <div className="sp-loading-header">
        <div className="sp-skeleton sp-skeleton-title" />
        <div className="sp-skeleton sp-skeleton-button" />
      </div>

      <div className="sp-loading-stats">
        {[1, 2, 3, 4].map((item) => (
          <div
            className="sp-skeleton-card"
            key={item}
          >
            <div className="sp-skeleton sp-skeleton-icon" />
            <div className="sp-skeleton sp-skeleton-line large" />
            <div className="sp-skeleton sp-skeleton-line" />
          </div>
        ))}
      </div>

      <div className="sp-loading-table">
        <div className="sp-skeleton sp-skeleton-line large" />

        {[1, 2, 3, 4, 5].map((item) => (
          <div
            className="sp-loading-row"
            key={item}
          >
            <div className="sp-skeleton sp-skeleton-avatar" />
            <div className="sp-skeleton sp-skeleton-line large" />
            <div className="sp-skeleton sp-skeleton-line" />
            <div className="sp-skeleton sp-skeleton-line" />
          </div>
        ))}
      </div>
    </section>
  )
}

export default ProductLoading
