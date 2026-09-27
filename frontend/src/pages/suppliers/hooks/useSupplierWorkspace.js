import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import { useBusiness } from '../../../context/BusinessContext'
import { getSuppliers } from '../../../services/suppliers'

export function useSupplierWorkspace({
  setError,
}) {
  const {
    businesses,
    businessId,
    selectBusiness,
    loading: businessLoading,
  } = useBusiness()

  const [suppliers, setSuppliers] =
    useState([])

  const [search, setSearch] =
    useState('')

  const [loading, setLoading] =
    useState(true)

  useEffect(() => {
    if (!businessId) {
      return undefined
    }

    let active = true

    async function loadSuppliers() {
      try {
        setLoading(true)
        setError('')

        const data =
          await getSuppliers(businessId)

        if (!active) {
          return
        }

        setSuppliers(data)
      } catch (err) {
        if (!active) {
          return
        }

        setSuppliers([])

        setError(
          err.response?.data?.detail ||
            'Failed to load suppliers.',
        )
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadSuppliers()

    return () => {
      active = false
    }
  }, [businessId, setError])

  const filteredSuppliers =
    useMemo(() => {
      const query =
        search.trim().toLowerCase()

      if (!query) {
        return suppliers
      }

      return suppliers.filter(
        (supplier) =>
          String(
            supplier.name || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            supplier.phone || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            supplier.email || '',
          )
            .toLowerCase()
            .includes(query),
      )
    }, [suppliers, search])

  function handleBusinessChange(event) {
    selectBusiness(event.target.value)
  }

  function handleSearchChange(event) {
    setSearch(event.target.value)
  }

  return {
    businesses,
    businessId,
    suppliers,
    setSuppliers,
    search,
    loading:
      businessLoading || loading,
    filteredSuppliers,
    handleBusinessChange,
    handleSearchChange,
  }
}
