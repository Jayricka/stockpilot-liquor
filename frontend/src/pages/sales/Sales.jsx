import POS from '../../components/sales/POS'
import { useSalesWorkspace } from './hooks/useSalesWorkspace'

function Sales() {
  const {
    businesses,
    businessId,
    products,
    loading,
    error,
    business,
    handleBusinessChange,
    handleSaleCompleted,
  } = useSalesWorkspace()

  if (loading && !businessId) {
    return (
      <main className="sales-page">
        <div className="sales-loading">
          Loading sales...
        </div>
      </main>
    )
  }

  return (
    <main className="sales-page">
      <header className="sales-header">
        <div>
          <span className="sales-eyebrow">
            Point of sale
          </span>

          <h1>Sales</h1>

          <p>
            Create and complete customer sales.
          </p>
        </div>

        <label className="sales-business-selector">
          <span>Business</span>

          <select
            value={businessId}
            onChange={handleBusinessChange}
          >
            {businesses.map((item) => (
              <option
                key={item.id}
                value={item.id}
              >
                {item.name}
              </option>
            ))}
          </select>
        </label>
      </header>

      {error && (
        <div
          className="sales-error"
          role="alert"
        >
          {error}
        </div>
      )}

      {businessId && (
        <POS
          products={products}
          businessId={businessId}
          businessName={
            business?.name || 'Business'
          }
          loading={loading}
          onSaleCompleted={
            handleSaleCompleted
          }
        />
      )}
    </main>
  )
}

export default Sales
