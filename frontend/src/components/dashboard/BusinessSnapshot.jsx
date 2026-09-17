import {
  Package,
  Truck,
  AlertCircle,
} from 'lucide-react'

function BusinessSnapshot({ summary, purchases = [] }) {
  const items = [
    {
      label: 'Products',
      value: summary.total_products,
      icon: Package,
    },
    {
      label: 'Low stock',
      value: summary.low_stock_count,
      icon: AlertCircle,
    },
    {
      label: 'Deliveries',
      value: summary.pending_delivery_count,
      icon: Truck,
    },
    {
      label: 'Purchases',
      value: purchases.length,
      icon: Package,
    },
  ]

  return (
    <article className="dashboard-card">
      <div className="card-heading">
        <div>
          <span>Operations</span>
          <h2>Business snapshot</h2>
        </div>
      </div>

      <div className="snapshot-grid">
        {items.map((item) => {
          const Icon = item.icon

          return (
            <div className="snapshot-item" key={item.label}>
              <Icon size={17} />
              <strong>{item.value}</strong>
              <span>{item.label}</span>
            </div>
          )
        })}
      </div>
    </article>
  )
}

export default BusinessSnapshot
