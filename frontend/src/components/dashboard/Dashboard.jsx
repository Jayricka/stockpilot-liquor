import {
  useEffect,
  useState,
} from 'react'

import { useBusiness } from '../../context/BusinessContext'
import { getDashboard } from '../../services/dashboard'

import DashboardHeader from '../../components/dashboard/DashboardHeader'
import DashboardLoading from '../../components/dashboard/DashboardLoading'
import MetricCard from '../../components/dashboard/MetricCard'
import PaymentMethods from '../../components/dashboard/PaymentMethods'
import LowStock from '../../components/dashboard/LowStock'
import RecentSales from '../../components/dashboard/RecentSales'
import BusinessSnapshot from '../../components/dashboard/BusinessSnapshot'
import TopProducts from '../../components/dashboard/TopProducts'

function Dashboard() {
  const {
    businesses,
    businessId,
    selectBusiness,
    loading: businessLoading,
  } = useBusiness()

  const [dashboard, setDashboard] =
    useState(null)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')

  useEffect(() => {
    if (!businessId) {
      return undefined
    }

    let active = true

    async function loadDashboard() {
      try {
        setLoading(true)
        setError('')

        const data =
          await getDashboard(businessId)

        if (!active) {
          return
        }

        setDashboard(data)
      } catch {
        if (!active) {
          return
        }

        setDashboard(null)
        setError(
          'Unable to load dashboard data.',
        )
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadDashboard()

    return () => {
      active = false
    }
  }, [businessId])

  if (
    businessLoading ||
    (loading && !dashboard)
  ) {
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
          <p>
            Create a business to start using
            StockPilot.
          </p>
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
        onBusinessChange={selectBusiness}
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
          payments={
            dashboard.sales_by_payment_method
          }
        />

        <LowStock
          products={dashboard.low_stock}
        />

        <RecentSales
          sales={dashboard.recent_sales}
        />

        <BusinessSnapshot
          summary={summary}
          purchases={dashboard.purchases}
        />

        <TopProducts
          products={dashboard.top_products}
        />
      </div>
    </section>
  )
}

export default Dashboard
