import {
  AlertTriangle,
  CheckCircle2,
  Package,
  XCircle,
} from 'lucide-react'

function ProductStats({ products = [] }) {
  const total = products.length

  const active = products.filter(
    (product) => Boolean(product.is_active),
  ).length

  const lowStock = products.filter(
    (product) => Boolean(product.is_low_stock),
  ).length

  const outOfStock = products.filter(
    (product) => Number(product.stock_quantity || 0) <= 0,
  ).length

  const stats = [
    {
      label: 'Total Products',
      value: total,
      detail: 'Products in catalog',
      icon: Package,
    },
    {
      label: 'Active',
      value: active,
      detail: 'Currently available',
      icon: CheckCircle2,
    },
    {
      label: 'Low Stock',
      value: lowStock,
      detail: 'Need attention',
      icon: AlertTriangle,
    },
    {
      label: 'Out of Stock',
      value: outOfStock,
      detail: 'Currently unavailable',
      icon: XCircle,
    },
  ]

  return (
    <section className="product-stats">
      {stats.map((stat) => {
        const Icon = stat.icon

        return (
          <article
            key={stat.label}
            className="product-stat-card"
          >
            <div className="product-stat-top">
              <div className="product-stat-icon">
                <Icon size={18} />
              </div>

              <span className="product-stat-label">
                {stat.label}
              </span>
            </div>

            <div className="product-stat-value">
              {stat.value}
            </div>

            <p className="product-stat-detail">
              {stat.detail}
            </p>
          </article>
        )
      })}
    </section>
  )
}

export default ProductStats
