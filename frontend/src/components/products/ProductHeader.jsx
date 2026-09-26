import { PackagePlus } from 'lucide-react'

function ProductHeader({
  businesses = [],
  businessId = '',
  onBusinessChange,
  productCount = 0,
  onAddProduct,
}) {
  return (
    <header className="product-header">
      <div className="product-header-content">
        <div className="product-header-copy">
          <div className="product-header-icon">
            <PackagePlus size={20} />
          </div>

          <div>
            <h1>Products</h1>
            <p>
              Manage your product catalog, pricing, stock, and availability.
            </p>
          </div>
        </div>

        <div className="product-header-actions">
          {businesses.length > 0 && (
            <select
              value={businessId}
              onChange={(event) =>
                onBusinessChange(event.target.value)
              }
              className="product-business-select"
              aria-label="Select business"
            >
              {businesses.map((business) => (
                <option
                  key={business.id}
                  value={business.id}
                >
                  {business.name}
                </option>
              ))}
            </select>
          )}

          <button
            type="button"
            className="product-create-button"
            onClick={onAddProduct}
          >
            <PackagePlus size={17} />
            <span>Add Product</span>
          </button>
        </div>
      </div>

      <div className="product-header-meta">
        {productCount} {productCount === 1 ? 'product' : 'products'}
      </div>
    </header>
  )
}

export default ProductHeader
