function formatCurrency(value) {
  return `KES ${Number(value || 0).toLocaleString()}`
}

function ReportSummary({ summary }) {
  const metrics = [
    {
      label: "Today's Revenue",
      value: formatCurrency(
        summary.today_revenue,
      ),
    },
    {
      label: 'Gross Profit',
      value: formatCurrency(
        summary.today_gross_profit,
      ),
    },
    {
      label: "Today's Sales",
      value: summary.today_sales_count,
    },
    {
      label: 'Stock Value',
      value: formatCurrency(
        summary.total_stock_value,
      ),
    },
    {
      label: 'Products',
      value: summary.total_products,
    },
    {
      label: 'Low Stock',
      value: summary.low_stock_count,
    },
    {
      label: 'Pending Deliveries',
      value: summary.pending_delivery_count,
    },
  ]

  return (
    <div className="reports-summary">
      {metrics.map((metric) => (
        <article
          className="report-metric"
          key={metric.label}
        >
          <span>{metric.label}</span>
          <strong>{metric.value}</strong>
        </article>
      ))}
    </div>
  )
}

export default ReportSummary
