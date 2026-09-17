import { useEffect, useState } from 'react'

import {
  getBusinesses,
  getDashboard,
} from '../../services/dashboard'

import DashboardHeader from '../../components/dashboard/DashboardHeader'
import DashboardLoading from '../../components/dashboard/DashboardLoading'
import MetricCard from '../../components/dashboard/MetricCard'
import PaymentMethods from '../../components/dashboard/PaymentMethods'
import LowStock from '../../components/dashboard/LowStock'
import RecentSales from '../../components/dashboard/RecentSales'
import BusinessSnapshot from '../../components/dashboard/BusinessSnapshot'
import TopProducts from '../../components/dashboard/TopProducts'

function Dashboard() {
  const [businesses, setBusinesses] = useState([])
  const [businessId, setBusinessId] = useState(null)
  const [dashboard, setDashboard] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadBusinesses() {
      try {
        const data = await getBusinesses()
        setBusinesses(data)

        if (data.length) {
          setBusinessId(data[0].id)
        }
      } catch {
        setError('Unable to load your businesses.')
      }
    }

    loadBusinesses()
  }, [])

  useEffect(() => {
    if (!businessId) return

    async function loadDashboard() {
      setLoading(true)
      setError('')

      try {
        const data = await getDashboard(businessId)
        setDashboard(data)
      } catch {
        setError('Unable to load dashboard data.')
      } finally {
        setLoading(false)
      }
    }

    loadDashboard()
  }, [businessId])

  if (loading && !dashboard) {
    return <DashboardLoading />
  }

  if (error && !dashboard) {
    return (
      <section className="dashboard-page">
        <div className="dashboard-error">
          <h2>Something went wrong</h2>
          <p>{error}</p>
        </div>
      </section>
    )
  }

  if (!dashboard) {
    return (
      <section className="dashboard-page">
        <div className="dashboard-empty">
          <h2>No business found</h2>
          <p>Create a business to start using StockPilot.</p>
        </div>
      </section>
    )
  }

  const { summary } = dashboard

  return (
    <section className="dashboard-page">
      <DashboardHeader
        businesses={businesses}
        businessId={businessId}
        onBusinessChange={setBusinessId}
        date={dashboard.date}
      />

      <div className="dashboard-metrics">
        <MetricCard
          label="Today's revenue"
          value={summary.today_revenue}
          type="currency"
        />

        <MetricCard
          label="Gross profit"
          value={summary.today_gross_profit}
          type="currency"
        />

        <MetricCard
          label="Today's sales"
          value={summary.today_sales_count}
        />

        <MetricCard
          label="Stock value"
          value={summary.total_stock_value}
          type="currency"
        />
      </div>

      <div className="dashboard-grid">
        <PaymentMethods
          payments={dashboard.sales_by_payment_method}
        />

        <LowStock
          products={dashboard.low_stock_products}
        />
      </div>

      <div className="dashboard-grid">
        <RecentSales
          sales={dashboard.recent_sales}
        />

        <BusinessSnapshot
          summary={summary}
          purchases={dashboard.recent_purchases}
        />
      </div>

      <TopProducts
        products={dashboard.top_products}
      />
    </section>
  )
}

export default Dashboard
