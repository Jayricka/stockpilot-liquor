/* eslint-disable react-hooks/set-state-in-effect */

import {
  useCallback,
  useEffect,
  useState,
} from 'react'

import POS from '../../components/sales/POS'

import {
  getProducts,
} from '../../services/products'

import {
  getBusinesses,
} from '../../services/dashboard'

function normalizeList(data) {
  if (Array.isArray(data)) {
    return data
  }

  return data?.results || []
}

function getErrorMessage(error) {
  const data = error?.response?.data

  if (!data) {
    return 'Something went wrong. Please try again.'
  }

  if (typeof data.detail === 'string') {
    return data.detail
  }

  if (Array.isArray(data.detail)) {
    return data.detail.join(', ')
  }

  if (Array.isArray(data.non_field_errors)) {
    return data.non_field_errors.join(', ')
  }

  const firstError = Object.values(data)[0]

  if (Array.isArray(firstError)) {
    return firstError.join(', ')
  }

  if (typeof firstError === 'string') {
    return firstError
  }

  return 'Something went wrong. Please try again.'
}

function Sales() {
  const [businesses, setBusinesses] =
    useState([])

  const [businessId, setBusinessId] =
    useState('')

  const [products, setProducts] =
    useState([])

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState('')

  const loadBusinesses = useCallback(
    async () => {
      try {
        setError('')

        const data = await getBusinesses()
        const list = normalizeList(data)

        setBusinesses(list)

        if (
          list.length &&
          !businessId
        ) {
          setBusinessId(
            String(list[0].id),
          )
        }
      } catch (requestError) {
        setError(
          getErrorMessage(requestError),
        )
      }
    },
    [businessId],
  )

  const loadProducts = useCallback(
    async (selectedBusinessId) => {
      if (!selectedBusinessId) {
        setProducts([])
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const data = await getProducts(
          selectedBusinessId,
        )

        const list = normalizeList(data)

        setProducts(
          list.filter(
            (product) =>
              product.is_active,
          ),
        )
      } catch (requestError) {
        setProducts([])
        setError(
          getErrorMessage(requestError),
        )
      } finally {
        setLoading(false)
      }
    },
    [],
  )

  useEffect(() => {
    loadBusinesses()
  }, [loadBusinesses])

  useEffect(() => {
    loadProducts(businessId)
  }, [businessId, loadProducts])

  function handleBusinessChange(event) {
    setBusinessId(event.target.value)
  }

  function handleSaleCompleted() {
    loadProducts(businessId)
  }

  const business = businesses.find(
    (item) =>
      String(item.id) ===
      String(businessId),
  )

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
            Create and complete customer
            sales.
          </p>
        </div>

        <label className="sales-business-selector">
          <span>Business</span>

          <select
            value={businessId}
            onChange={
              handleBusinessChange
            }
          >
            {businesses.map(
              (item) => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name}
                </option>
              ),
            )}
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
            business?.name ||
            'Business'
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
