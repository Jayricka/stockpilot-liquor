import { Edit3 } from 'lucide-react'

function formatCurrency(value) {
  const amount = Number(value || 0)

  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    maximumFractionDigits: 0,
  }).format(amount)
}

function formatQuantity(value) {
  const amount = Number(value || 0)

  return new Intl.NumberFormat('en-KE', {
    maximumFractionDigits: 2,
  }).format(amount)
}

function getStockState(product) {
  const quantity = Number(
    product.stock_quantity || 0,
  )

  const reorderLevel = Number(
    product.reorder_level || 0,
  )

  if (quantity <= 0) {
    return {
      label: 'Out of stock',
      state: 'out',
    }
  }

  if (quantity <= reorderLevel) {
    return {
      label: 'Low stock',
      state: 'low',
    }
  }

  return {
    label: 'In stock',
    state: 'in',
  }
}

function StockIndicator({ product }) {
  const stockState = getStockState(product)

  const unit = String(
    product.unit || 'piece',
  ).toLowerCase()

  return (
    <div className="product-stock">
      <div className="product-stock-quantity">
        {formatQuantity(product.stock_quantity)}

        <span>
          {unit}
        </span>
      </div>

      <span
        className={`product-stock-badge product-stock-${stockState.state}`}
      >
        <span className="product-stock-dot" />
        {stockState.label}
      </span>
    </div>
  )
}

function StatusBadge({ active }) {
  return (
    <span
      className={`product-status-badge ${
        active
          ? 'product-status-active'
          : 'product-status-inactive'
      }`}
    >
      <span className="product-status-dot" />
      {active ? 'Active' : 'Inactive'}
    </span>
  )
}

function getInitials(name) {
  return (
    name
      ?.split(' ')
      .slice(0, 2)
      .map((word) => word.charAt(0))
      .join('')
      .toUpperCase() || 'P'
  )
}

function ProductRow({ product, onEdit }) {
  const initials = getInitials(product.name)

  return (
    <tr className="product-table-row">
      <td>
        <div className="product-row-product">
          <div className="product-row-avatar">
            {initials}
          </div>

          <div className="product-row-copy">
            <p className="product-row-name">
              {product.name}
            </p>

            {product.brand && (
              <p className="product-row-brand">
                {product.brand}
              </p>
            )}
          </div>
        </div>
      </td>

      <td>
        <span className="product-row-category">
          {product.category_name ||
            'Uncategorized'}
        </span>
      </td>

      <td>
        <span className="product-row-sku">
          {product.sku || '—'}
        </span>
      </td>

      <td className="product-row-price-cell">
        <span className="product-row-price">
          {formatCurrency(
            product.selling_price,
          )}
        </span>

        <span className="product-row-unit">
          / {String(
            product.unit || 'unit',
          ).toLowerCase()}
        </span>
      </td>

      <td>
        <StockIndicator product={product} />
      </td>

      <td>
        <StatusBadge
          active={Boolean(product.is_active)}
        />
      </td>

      <td className="product-row-actions">
        <button
          type="button"
          onClick={() => onEdit(product)}
          aria-label={`Edit ${product.name}`}
          title="Edit product"
          className="product-edit-button"
        >
          <Edit3 size={15} />
        </button>
      </td>
    </tr>
  )
}

export default ProductRow
