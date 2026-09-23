function getStockStatus(product) {
  const stock = Number(product.stock_quantity || 0)
  const reorderLevel = Number(product.reorder_level || 0)

  if (stock === 0) {
    return {
      label: 'Out of stock',
      className: 'status-danger',
    }
  }

  if (stock <= reorderLevel) {
    return {
      label: 'Low stock',
      className: 'status-warning',
    }
  }

  return {
    label: 'In stock',
    className: 'status-success',
  }
}

function InventoryTable({ products }) {
  return (
    <article className="inventory-table-card">
      <div className="inventory-table-heading">
        <div>
          <span>Product catalogue</span>
          <h2>All products</h2>
        </div>

        <span className="inventory-count">
          {products.length} products
        </span>
      </div>

      <div className="inventory-table-wrapper">
        <table className="inventory-table">
          <thead>
            <tr>
              <th>Product</th>
              <th>SKU</th>
              <th>Category</th>
              <th>Stock</th>
              <th>Buying price</th>
              <th>Selling price</th>
              <th>Status</th>
            </tr>
          </thead>

          <tbody>
            {products.map((product) => {
              const status = getStockStatus(product)

              return (
                <tr key={product.id}>
                  <td>
                    <strong>{product.name}</strong>
                  </td>

                  <td>{product.sku || '—'}</td>

                  <td>
                    {product.category_name ||
                      product.category?.name ||
                      'Uncategorized'}
                  </td>

                  <td>
                    {product.stock_quantity || 0}{' '}
                    {product.unit || ''}
                  </td>

                  <td>
                    KES{' '}
                    {Number(
                      product.buying_price || 0,
                    ).toLocaleString()}
                  </td>

                  <td>
                    KES{' '}
                    {Number(
                      product.selling_price || 0,
                    ).toLocaleString()}
                  </td>

                  <td>
                    <span
                      className={`inventory-status ${status.className}`}
                    >
                      {status.label}
                    </span>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>

      {!products.length && (
        <div className="inventory-empty">
          <h3>No products found</h3>
          <p>
            Try changing your search or filter.
          </p>
        </div>
      )}
    </article>
  )
}

export default InventoryTable
