import { TrendingUp } from 'lucide-react'

function formatCurrency(value) {
  return `KES ${Number(value || 0).toLocaleString()}`
}

function MetricCard({ label, value, type }) {
  const displayValue =
    type === 'currency'
      ? formatCurrency(value)
      : Number(value || 0).toLocaleString()

  return (
    <article className="metric-card">
      <div className="metric-card-top">
        <span>{label}</span>

        <span className="metric-icon">
          <TrendingUp size={16} />
        </span>
      </div>

      <strong>{displayValue}</strong>
    </article>
  )
}

export default MetricCard
