import {
  PackageOpen,
  SearchX,
} from 'lucide-react'

function ProductEmptyState({
  hasFilters,
  onClear,
  onAddProduct,
}) {
  if (hasFilters) {
    return (
      <div className="product-empty-state">
        <div className="product-empty-icon">
          <SearchX size={22} />
        </div>

        <h3>No products found</h3>

        <p>
          Nothing matches your current search
          and filters. Try adjusting your
          selection.
        </p>

        <button
          type="button"
          onClick={onClear}
          className="product-empty-secondary"
        >
          Clear filters
        </button>
      </div>
    )
  }

  return (
    <div className="product-empty-state">
      <div className="product-empty-icon">
        <PackageOpen size={22} />
      </div>

      <h3>No products yet</h3>

      <p>
        Add your first product to start
        managing your catalogue and inventory.
      </p>

      <button
        type="button"
        onClick={onAddProduct}
        className="product-empty-primary"
      >
        Add product
      </button>
    </div>
  )
}

export default ProductEmptyState
