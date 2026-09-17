import { AlertTriangle } from 'lucide-react'

function LowStock({ products = [] }) {
  return (
    <article className="dashboard-card">
      <div className="card-heading">
        <div>
          <span>Inventory alert</span>
          <h2>Low stock</h2>
        </div>

        <AlertTriangle size={18} />
      </div>

      <div className="stock-list">
        {products.length ? (
          products.map((product) => (
            <div className="stock-row" key={product.id}>
              <div>
                <strong>{product.name}</strong>
                <span>{product.sku}</span>
              </div>

              <div className="stock-quantity">
                <strong>{product.stock_quantity}</strong>
                <span>
                  / {product.reorder_level} {product.unit}
                </span>
              </div>
            </div>
          ))
        ) : (
          <p className="empty-message">
            Inventory levels look healthy.
          </p>
        )}
      </div>
    </article>
  )
}

export default LowStock
