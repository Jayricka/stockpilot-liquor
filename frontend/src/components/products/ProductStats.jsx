import {
  AlertTriangle,
  Boxes,
  CircleCheck,
  Wallet,
} from 'lucide-react'

function ProductStats({ products = [] }) {
  const total = products.length

  const active = products.filter(
    (product) => product.is_active,
  ).length

  const lowStock = products.filter(
    (product) => product.is_low_stock,
  ).length

  const inventoryValue = products.reduce(
    (totalValue, product) =>
      totalValue +
      Number(product.buying_price || 0) *
        Number(product.stock_quantity || 0),
    0,
  )

  const formatCurrency = (value) =>
    new Intl.NumberFormat('en-KE', {
      style: 'currency',
      currency: 'KES',
      maximumFractionDigits: 0,
    }).format(value)

  const stats = [
    {
      label: 'Total products',
      value: total,
      icon: Boxes,
      detail: 'Across your catalog',
      tone: 'neutral',
    },
    {
      label: 'Active products',
      value: active,
      icon: CircleCheck,
      detail: `${total ? Math.round((active / total) * 100) : 0}% of catalog`,
      tone: 'success',
    },
    {
      label: 'Low stock',
      value: lowStock,
      icon: AlertTriangle,
      detail: lowStock ? 'Needs attention' : 'Stock looks healthy',
      tone: lowStock ? 'warning' : 'success',
    },
    {
      label: 'Inventory value',
      value: formatCurrency(inventoryValue),
      icon: Wallet,
      detail: 'Based on buying price',
      tone: 'primary',
    },
  ]

  return (
    <section className="sp-product-stats">
      {stats.map((stat) => {
        const Icon = stat.icon

        return (
          <article
            className={`sp-stat-card sp-stat-${stat.tone}`}
            key={stat.label}
          >
            <div className="sp-stat-top">
              <div className="sp-stat-icon">
                <Icon size={18} />
              </div>

              <span className="sp-stat-label">
                {stat.label}
              </span>
            </div>

            <div className="sp-stat-value">
              {stat.value}
            </div>

            <div className="sp-stat-detail">
              {stat.detail}
            </div>
          </article>
        )
      })}
    </section>
  )
}

export default ProductStats
