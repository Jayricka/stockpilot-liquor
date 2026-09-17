function TopProducts({ products = [] }) {
  return (
    <article className="dashboard-card dashboard-wide">
      <div className="card-heading">
        <div>
          <span>Today's performance</span>
          <h2>Top products</h2>
        </div>
      </div>

      <div className="product-table">
        <div className="product-table-head">
          <span>Product</span>
          <span>Units sold</span>
          <span>Revenue</span>
        </div>

        {products.length ? (
          products.map((product) => (
            <div
              className="product-table-row"
              key={product.items__product_id}
            >
              <strong>{product.items__product__name}</strong>

              <span>
                {Number(product.quantity).toLocaleString()}
              </span>

              <span>
                KES {Number(product.revenue).toLocaleString()}
              </span>
            </div>
          ))
        ) : (
          <p className="empty-message">
            No product sales recorded today.
          </p>
        )}
      </div>
    </article>
  )
}

export default TopProducts
