import { useEffect, useState } from 'react'

import {
  getBusinesses,
} from '../../services/dashboard'

import {
  getReport,
} from '../../services/reports'

import ReportHeader from '../../components/reports/ReportHeader'
import ReportLoading from '../../components/reports/ReportLoading'
import ReportSummary from '../../components/reports/ReportSummary'
import PaymentBreakdown from '../../components/reports/PaymentBreakdown'
import TopProducts from '../../components/reports/TopProducts'
import LowStockReport from '../../components/reports/LowStockReport'
import RecentSales from '../../components/reports/RecentSales'
import RecentPurchases from '../../components/reports/RecentPurchases'

function Reports() {
  const [businesses, setBusinesses] =
    useState([])

  const [businessId, setBusinessId] =
    useState(null)

  const [report, setReport] =
    useState(null)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')

  useEffect(() => {
    async function loadBusinesses() {
      try {
        const data =
          await getBusinesses()

        setBusinesses(data)

        if (data.length) {
          setBusinessId(data[0].id)
        }
      } catch {
        setError(
          'Unable to load your businesses.',
        )
        setLoading(false)
      }
    }

    loadBusinesses()
  }, [])

  useEffect(() => {
    if (!businessId) {
      return
    }

    async function loadReport() {
      setLoading(true)
      setError('')

      try {
        const data =
          await getReport(businessId)

        setReport(data)
      } catch {
        setError(
          'Unable to load report data.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadReport()
  }, [businessId])

  if (loading && !report) {
    return <ReportLoading />
  }

  if (error && !report) {
    return (
      <section className="reports-page">
        <div className="reports-error">
          <h2>Something went wrong</h2>
          <p>{error}</p>
        </div>
      </section>
    )
  }

  if (!report) {
    return (
      <section className="reports-page">
        <div className="reports-empty">
          <h2>No business found</h2>

          <p>
            Create a business to generate
            reports.
          </p>
        </div>
      </section>
    )
  }

  return (
    <section className="reports-page">
      <ReportHeader
        businesses={businesses}
        businessId={businessId}
        onBusinessChange={setBusinessId}
        date={report.date}
      />

      {error && (
        <div
          className="reports-error reports-error-inline"
          role="alert"
        >
          {error}
        </div>
      )}

      <ReportSummary
        summary={report.summary}
      />

      <div className="reports-grid">
        <PaymentBreakdown
          payments={
            report.sales_by_payment_method
          }
        />

        <TopProducts
          products={report.top_products}
        />
      </div>

      <div className="reports-grid">
        <LowStockReport
          products={report.low_stock_products}
        />

        <RecentSales
          sales={report.recent_sales}
        />
      </div>

      <RecentPurchases
        purchases={report.recent_purchases}
      />
    </section>
  )
}

export default Reports
