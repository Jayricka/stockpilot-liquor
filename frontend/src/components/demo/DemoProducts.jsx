function DemoProducts({ products }) {
  return (
    <section className="demo-products-section">
      <div className="demo-section-heading">
        <div>
          <span className="demo-eyebrow">
            Live inventory
          </span>

          <h2>Products</h2>
        </div>

        <span>
          {products.length} products
        </span>
      </div>

      <div className="demo-products-table">
        <div className="demo-products-header">
          <span>Product</span>
          <span>Category</span>
          <span>Price</span>
          <span>Stock</span>
          <span>Status</span>
        </div>

        {products.map((product) => {
          const stock =
            Number(product.stock_quantity || 0)

          const reorderLevel =
            Number(product.reorder_level || 0)

          const lowStock =
            stock <= reorderLevel

          const category =
            typeof product.category === 'object'
              ? product.category?.name
              : product.category_name

          return (
            <div
              className="demo-product-row"
              key={product.id}
            >
              <div>
                <strong>
                  {product.name}
                </strong>

                {product.brand && (
                  <small>
                    {product.brand}
                  </small>
                )}
              </div>

              <span>
                {category || '—'}
              </span>

              <span>
                KES{' '}
                {Number(
                  product.selling_price || 0,
                ).toLocaleString()}
              </span>

              <strong>{stock}</strong>

              <span
                className={
                  lowStock
                    ? 'demo-stock-status is-low'
                    : 'demo-stock-status'
                }
              >
                {lowStock
                  ? 'Low stock'
                  : 'Healthy'}
              </span>
            </div>
          )
        })}
      </div>
    </section>
  )
}

export default DemoProducts
