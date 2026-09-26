function ProductTableLoading() {
  return (
    <>
      {Array.from({ length: 6 }).map((_, rowIndex) => (
        <tr
          key={rowIndex}
          className="product-table-row product-table-loading-row"
        >
          <td>
            <div className="product-loading-product">
              <div className="product-loading-avatar" />

              <div className="product-loading-copy">
                <div className="product-loading-line product-loading-line-wide" />
                <div className="product-loading-line product-loading-line-short" />
              </div>
            </div>
          </td>

          <td>
            <div className="product-loading-line product-loading-category" />
          </td>

          <td>
            <div className="product-loading-line product-loading-sku" />
          </td>

          <td>
            <div className="product-loading-line product-loading-price" />
          </td>

          <td>
            <div className="product-loading-stock" />
          </td>

          <td>
            <div className="product-loading-status" />
          </td>

          <td>
            <div className="product-loading-action" />
          </td>
        </tr>
      ))}
    </>
  )
}

export default ProductTableLoading
