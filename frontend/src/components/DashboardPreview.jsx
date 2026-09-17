import { Zap } from 'lucide-react'

function DashboardPreview() {
  return (
    <div className="dashboard-frame" id="product-preview">
      <div className="dashboard-topbar">
        <div className="dashboard-brand">
          <span className="mini-mark">
            <Zap size={13} />
          </span>

          StockPilot
        </div>

        <div className="dashboard-user">
          <span />
          Demo business
        </div>
      </div>

      <div className="dashboard-body">
        <aside className="dashboard-sidebar">
          <span className="sidebar-active">Overview</span>
          <span>Inventory</span>
          <span>Sales</span>
          <span>Purchases</span>
          <span>Suppliers</span>
          <span>Deliveries</span>
        </aside>

        <div className="dashboard-content">
          <div className="dashboard-heading">
            <div>
              <span>Tuesday, September 17</span>
              <h3>Good afternoon, owner</h3>
            </div>

            <span className="status-pill">Live preview</span>
          </div>

          <div className="metric-grid">
            <Metric
              label="Today's revenue"
              value="KES 48,250"
              trend="+12.4%"
            />

            <Metric
              label="Gross profit"
              value="KES 13,840"
              trend="+8.2%"
            />

            <Metric
              label="Total products"
              value="248"
              trend="Active"
            />
          </div>

          <div className="dashboard-lower">
            <SalesChart />
            <LowStock />
          </div>
        </div>
      </div>
    </div>
  )
}

function Metric({ label, value, trend }) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{trend}</small>
    </div>
  )
}

function SalesChart() {
  const bars = [36, 55, 42, 72, 61, 88, 76]
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

  return (
    <div className="chart-card">
      <div className="chart-card-heading">
        <span>Sales overview</span>
        <small>Last 7 days</small>
      </div>

      <div className="fake-chart">
        {bars.map((height, index) => (
          <span key={days[index]} style={{ height: `${height}%` }} />
        ))}
      </div>

      <div className="chart-days">
        {days.map((day) => (
          <small key={day}>{day}</small>
        ))}
      </div>
    </div>
  )
}

function LowStock() {
  const products = [
    ['Premium Vodka', '3 left'],
    ['Reserve Whisky', '5 left'],
    ['Classic Gin', '2 left'],
  ]

  return (
    <div className="low-stock-card">
      <div className="chart-card-heading">
        <span>Low stock</span>
        <small className="warning-text">4 items</small>
      </div>

      {products.map(([name, quantity]) => (
        <div className="stock-line" key={name}>
          <span>{name}</span>
          <strong>{quantity}</strong>
        </div>
      ))}
    </div>
  )
}

export default DashboardPreview
