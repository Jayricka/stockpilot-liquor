import {
  useEffect,
  useState,
} from 'react'

import {
  getReport,
} from '../../services/reports'

import {
  useBusiness,
} from '../../context/BusinessContext'

import ReportHeader from '../../components/reports/ReportHeader'
import ReportLoading from '../../components/reports/ReportLoading'
import ReportSummary from '../../components/reports/ReportSummary'
import PaymentBreakdown from '../../components/reports/PaymentBreakdown'
import TopProducts from '../../components/reports/TopProducts'
import LowStockReport from '../../components/reports/LowStockReport'
import RecentSales from '../../components/reports/RecentSales'
import RecentPurchases from '../../components/reports/RecentPurchases'

function Reports() {
  const {
    businesses,
    businessId,
    selectBusiness,
    loading: businessLoading,
  } = useBusiness()

  const [report, setReport] =
    useState(null)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')

  useEffect(() => {
    let active = true

    if (!businessId) {
      return () => {
        active = false
      }
    }

    async function loadReport() {
      try {
        setLoading(true)
        setError('')

        const data =
          await getReport(businessId)

        if (!active) {
          return
        }

        setReport(data)
      } catch {
        if (!active) {
          return
        }

        setReport(null)
        setError(
          'Unable to load report data.',
        )
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadReport()

    return () => {
      active = false
    }
  }, [businessId])

  function handleBusinessChange(event) {
    selectBusiness(event.target.value)
  }

  if (
    businessLoading ||
    (loading && !report)
  ) {
    return <ReportLoading />
  }

  if (error && !report) {
    return (
      <section className="reports-page">
        <ReportHeader
          businesses={businesses}
          businessId={businessId}
          onBusinessChange={
            handleBusinessChange
          }
        />

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
        <ReportHeader
          businesses={businesses}
          businessId={businessId}
          onBusinessChange={
            handleBusinessChange
          }
        />

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
        onBusinessChange={
          handleBusinessChange
        }
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
          products={
            report.low_stock_products
          }
        />

        <RecentSales
          sales={report.recent_sales}
        />

        <RecentPurchases
          purchases={
            report.recent_purchases
          }
        />
      </div>
    </section>
  )
}

export default Reports
