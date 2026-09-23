function TopProducts({ products }) {
  return (
    <article className="report-panel">
      <div className="report-panel-header">
        <div>
          <span>PERFORMANCE</span>
          <h2>Top products</h2>
        </div>

        <span>Today</span>
      </div>

      {!products.length ? (
        <p className="report-empty">
          No product sales recorded today.
        </p>
      ) : (
        <div className="report-table-wrap">
          <table className="report-table">
            <thead>
              <tr>
                <th>Product</th>
                <th>Quantity</th>
                <th>Revenue</th>
              </tr>
            </thead>

            <tbody>
              {products.map((product) => (
                <tr
                  key={product.items__product_id}
                >
                  <td>
                    <strong>
                      {product.items__product__name}
                    </strong>
                  </td>

                  <td>
                    {Number(
                      product.quantity || 0,
                    ).toLocaleString()}
                  </td>

                  <td>
                    KES{' '}
                    {Number(
                      product.revenue || 0,
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

export default TopProducts
