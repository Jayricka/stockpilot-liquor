import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import { useBusiness } from '../../../context/BusinessContext'
import { getProducts } from '../../../services/products'
import { getSuppliers } from '../../../services/suppliers'
import { getPurchases } from '../../../services/purchases'

export function usePurchaseWorkspace(status) {
  const {
    businesses,
    businessId,
    selectBusiness,
    loading: businessLoading,
  } = useBusiness()

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
    let active = true

    async function loadWorkspace() {
      if (!businessId) {
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

        if (!active) {
          return
        }

        setPurchases(purchaseData)
        setSuppliers(supplierData)
        setProducts(productData)
      } catch (err) {
        if (!active) {
          return
        }

        setError(
          err.response?.data?.detail ||
            'Failed to load purchases.',
        )
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadWorkspace()

    return () => {
      active = false
    }
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

  function handleBusinessChange(event) {
    selectBusiness(event.target.value)
  }

  return {
    businesses,
    businessId,
    selectBusiness: handleBusinessChange,
    suppliers,
    products,
    search,
    setSearch,
    loading:
      businessLoading || loading,
    error,
    setError,
    filteredPurchases,
    setPurchases,
  }
}
