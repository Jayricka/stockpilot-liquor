import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import { getBusinesses } from '../../../services/dashboard'
import { getSuppliers } from '../../../services/suppliers'

export function useSupplierWorkspace({
  setError,
}) {
  const [businesses, setBusinesses] =
    useState([])

  const [businessId, setBusinessId] =
    useState('')

  const [suppliers, setSuppliers] =
    useState([])

  const [search, setSearch] =
    useState('')

  const [loading, setLoading] =
    useState(true)

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
  }, [setError])

  useEffect(() => {
    async function loadSuppliers() {
      if (!businessId) {
        setSuppliers([])
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const data =
          await getSuppliers(businessId)

        setSuppliers(data)
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Failed to load suppliers.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadSuppliers()
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
    setBusinessId(event.target.value)
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
    loading,
    filteredSuppliers,
    handleBusinessChange,
    handleSearchChange,
  }
}
