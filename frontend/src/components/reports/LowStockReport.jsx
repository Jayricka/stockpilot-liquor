function LowStockReport({
  products,
}) {
  return (
    <article className="report-panel">
      <div className="report-panel-header">
        <div>
          <span>INVENTORY</span>
          <h2>Low stock</h2>
        </div>

        <strong>
          {products.length}
        </strong>
      </div>

      {!products.length ? (
        <p className="report-empty">
          All active products are above
          their reorder levels.
        </p>
      ) : (
        <div className="report-table-wrap">
          <table className="report-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Stock</th>
                <th>Reorder</th>
              </tr>
            </thead>

            <tbody>
              {products.map((product) => (
                <tr key={product.id}>
                  <td>
                    <strong>
                      {product.name}
                    </strong>

                    <small>
                      {product.sku || 'No SKU'}
                    </small>
                  </td>

                  <td className="report-stock-low">
                    {Number(
                      product.stock_quantity || 0,
                    ).toLocaleString()}{' '}
                    {product.unit}
                  </td>

                  <td>
                    {Number(
                      product.reorder_level || 0,
                    ).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </article>
  )
}

export default LowStockReport
