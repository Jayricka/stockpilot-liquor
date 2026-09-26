import ProductEmptyState from './ProductEmptyState'
import ProductRow from './ProductRow'
import ProductTableLoading from './ProductTableLoading'

function ProductTable({
  products = [],
  loading = false,
  hasFilters = false,
  onClear,
  onEdit,
  onAddProduct,
}) {
  if (loading) {
    return (
      <section className="product-table">
        <div className="product-table-scroll">
          <table className="product-table-grid">
            <ProductTableHead />
            <tbody>
              <ProductTableLoading />
            </tbody>
          </table>
        </div>
      </section>
    )
  }

  if (!products.length) {
    return (
      <section className="product-table">
        <ProductEmptyState
          hasFilters={hasFilters}
          onClear={onClear}
          onAddProduct={onAddProduct}
        />
      </section>
    )
  }

  return (
    <section className="product-table">
      <div className="product-table-scroll">
        <table className="product-table-grid">
          <ProductTableHead />

          <tbody className="product-table-body">
            {products.map((product) => (
              <ProductRow
                key={product.id}
                product={product}
                onEdit={onEdit}
              />
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

function ProductTableHead() {
  return (
    <thead className="product-table-head">
      <tr>
        <th scope="col">Product</th>
        <th scope="col">Category</th>
        <th scope="col">SKU</th>
        <th scope="col">Price</th>
        <th scope="col">Stock</th>
        <th scope="col">Status</th>
        <th scope="col">Actions</th>
      </tr>
    </thead>
  )
}

export default ProductTable
