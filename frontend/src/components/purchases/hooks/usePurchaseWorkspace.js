import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import { getBusinesses } from '../../../services/dashboard'
import { getProducts } from '../../../services/products'
import { getSuppliers } from '../../../services/suppliers'
import { getPurchases } from '../../../services/purchases'

export function usePurchaseWorkspace(status) {
  const [businesses, setBusinesses] =
    useState([])

  const [businessId, setBusinessId] =
    useState('')

  const [purchases, setPurchases] =
    useState([])

  const [suppliers, setSuppliers] =
    useState([])

  const [products, setProducts] =
    useState([])

  const [search, setSearch] =
    useState('')

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
          setBusinessId(
            String(data[0].id),
          )
        }
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Failed to load businesses.',
        )
      }
    }

    loadBusinesses()
  }, [])

  useEffect(() => {
    async function loadWorkspace() {
      if (!businessId) {
        setPurchases([])
        setSuppliers([])
        setProducts([])
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const [
          purchaseData,
          supplierData,
          productData,
        ] = await Promise.all([
          getPurchases(
            businessId,
            status,
          ),
          getSuppliers(businessId),
          getProducts(businessId),
        ])

        setPurchases(purchaseData)
        setSuppliers(supplierData)
        setProducts(productData)
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Failed to load purchases.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadWorkspace()
  }, [businessId, status])

  const filteredPurchases =
    useMemo(() => {
      const query =
        search.trim().toLowerCase()

      if (!query) {
        return purchases
      }

      return purchases.filter(
        (purchase) =>
          String(
            purchase.reference_number || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            purchase.supplier_name || '',
          )
            .toLowerCase()
            .includes(query),
      )
    }, [purchases, search])

  return {
    businesses,
    businessId,
    setBusinessId,
    purchases,
    setPurchases,
    suppliers,
    products,
    search,
    setSearch,
    loading,
    error,
    setError,
    filteredPurchases,
  }
}
