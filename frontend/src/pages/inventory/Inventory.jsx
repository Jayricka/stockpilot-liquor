import { useEffect, useMemo, useState } from 'react'

import {
  getBusinesses,
} from '../../services/dashboard'

import {
  getProducts,
} from '../../services/inventory'

import InventoryHeader from '../../components/inventory/InventoryHeader'
import InventoryFilters from '../../components/inventory/InventoryFilters'
import InventoryStats from '../../components/inventory/InventoryStats'
import InventoryTable from '../../components/inventory/InventoryTable'
import InventoryLoading from '../../components/inventory/InventoryLoading'

function Inventory() {
  const [businesses, setBusinesses] = useState([])
  const [businessId, setBusinessId] = useState(null)
  const [products, setProducts] = useState([])
  const [search, setSearch] = useState('')
  const [lowStockOnly, setLowStockOnly] = useState(false)
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
        setLoading(false)
      }
    }

    loadBusinesses()
  }, [])

  useEffect(() => {
    if (!businessId) return

    async function loadProducts() {
      setLoading(true)
      setError('')

      try {
        const data = await getProducts(businessId)

        setProducts(
          Array.isArray(data)
            ? data
            : data.results || [],
        )
      } catch {
        setError('Unable to load inventory.')
      } finally {
        setLoading(false)
      }
    }

    loadProducts()
  }, [businessId])

  const filteredProducts = useMemo(() => {
    const query = search.toLowerCase().trim()

    return products.filter((product) => {
      const matchesSearch =
        !query ||
        product.name?.toLowerCase().includes(query) ||
        product.sku?.toLowerCase().includes(query)

      const matchesStock =
        !lowStockOnly ||
        Number(product.stock_quantity || 0) <=
          Number(product.reorder_level || 0)

      return matchesSearch && matchesStock
    })
  }, [products, search, lowStockOnly])

  if (loading && !products.length) {
    return <InventoryLoading />
  }

  return (
    <section className="inventory-page">
      <InventoryHeader
        businesses={businesses}
        businessId={businessId}
        onBusinessChange={setBusinessId}
      />

      {error && (
        <div className="inventory-error">
          {error}
        </div>
      )}

      <InventoryStats products={products} />

      <InventoryFilters
        search={search}
        onSearchChange={setSearch}
        lowStockOnly={lowStockOnly}
        onLowStockChange={setLowStockOnly}
      />

      <InventoryTable products={filteredProducts} />
    </section>
  )
}

export default Inventory
