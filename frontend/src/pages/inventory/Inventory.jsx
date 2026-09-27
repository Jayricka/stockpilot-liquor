import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import {
  getProducts,
} from '../../services/inventory'

import {
  useBusiness,
} from '../../context/BusinessContext'

import InventoryHeader from '../../components/inventory/InventoryHeader'
import InventoryFilters from '../../components/inventory/InventoryFilters'
import InventoryStats from '../../components/inventory/InventoryStats'
import InventoryTable from '../../components/inventory/InventoryTable'
import InventoryLoading from '../../components/inventory/InventoryLoading'

function Inventory() {
  const {
    businesses,
    businessId,
    selectBusiness,
    loading: businessLoading,
  } = useBusiness()

  const [products, setProducts] =
    useState([])

  const [search, setSearch] =
    useState('')

  const [lowStockOnly, setLowStockOnly] =
    useState(false)

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

    async function loadProducts() {
      try {
        setLoading(true)
        setError('')

        const data =
          await getProducts(businessId)

        if (!active) {
          return
        }

        setProducts(
          Array.isArray(data)
            ? data
            : data.results || [],
        )
      } catch {
        if (!active) {
          return
        }

        setProducts([])
        setError(
          'Unable to load inventory.',
        )
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadProducts()

    return () => {
      active = false
    }
  }, [businessId])

  const filteredProducts = useMemo(() => {
    const query =
      search.toLowerCase().trim()

    return products.filter((product) => {
      const matchesSearch =
        !query ||
        product.name
          ?.toLowerCase()
          .includes(query) ||
        product.sku
          ?.toLowerCase()
          .includes(query)

      const matchesStock =
        !lowStockOnly ||
        Number(
          product.stock_quantity || 0,
        ) <=
          Number(
            product.reorder_level || 0,
          )

      return (
        matchesSearch &&
        matchesStock
      )
    })
  }, [
    products,
    search,
    lowStockOnly,
  ])

  function handleBusinessChange(value) {
    selectBusiness(value)
  }

  if (
    businessLoading ||
    (loading && !products.length)
  ) {
    return <InventoryLoading />
  }

  return (
    <section className="inventory-page">
      <InventoryHeader
        businesses={businesses}
        businessId={businessId}
        onBusinessChange={
          handleBusinessChange
        }
      />

      {error && (
        <div className="inventory-error">
          {error}
        </div>
      )}

      <InventoryStats
        products={products}
      />

      <InventoryFilters
        search={search}
        onSearchChange={setSearch}
        lowStockOnly={lowStockOnly}
        onLowStockChange={
          setLowStockOnly
        }
      />

      <InventoryTable
        products={filteredProducts}
      />
    </section>
  )
}

export default Inventory
