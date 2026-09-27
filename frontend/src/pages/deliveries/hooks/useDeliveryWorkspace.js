import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import {
  getBusinessMembers,
  getDeliveries,
} from '../../../services/deliveries'

import { getBusinesses } from '../../../services/dashboard'
import { getSales } from '../../../services/sales'

function getErrorMessage(
  error,
  fallback,
) {
  return (
    error.response?.data?.detail ||
    fallback
  )
}

function useDeliveryWorkspace() {
  const [businesses, setBusinesses] =
    useState([])

  const [businessId, setBusinessId] =
    useState('')

  const [deliveries, setDeliveries] =
    useState([])

  const [sales, setSales] =
    useState([])

  const [members, setMembers] =
    useState([])

  const [search, setSearch] =
    useState('')

  const [status, setStatus] =
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
          getErrorMessage(
            err,
            'Failed to load businesses.',
          ),
        )
      }
    }

    loadBusinesses()
  }, [])

  useEffect(() => {
    async function loadWorkspace() {
      if (!businessId) {
        setDeliveries([])
        setSales([])
        setMembers([])
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const [
          deliveryData,
          salesData,
          memberData,
        ] = await Promise.all([
          getDeliveries(
            businessId,
            status,
          ),
          getSales(businessId, {
            status: 'COMPLETED',
          }),
          getBusinessMembers(
            businessId,
          ),
        ])

        setDeliveries(deliveryData)
        setSales(salesData)
        setMembers(memberData)
      } catch (err) {
        setError(
          getErrorMessage(
            err,
            'Failed to load deliveries.',
          ),
        )
      } finally {
        setLoading(false)
      }
    }

    loadWorkspace()
  }, [businessId, status])

  const availableSales =
    useMemo(() => {
      const deliverySaleIds =
        new Set(
          deliveries.map(
            (delivery) =>
              Number(delivery.sale),
          ),
        )

      return sales.filter(
        (sale) =>
          !deliverySaleIds.has(
            Number(sale.id),
          ),
      )
    }, [sales, deliveries])

  const filteredDeliveries =
    useMemo(() => {
      const query =
        search.trim().toLowerCase()

      if (!query) {
        return deliveries
      }

      return deliveries.filter(
        (delivery) =>
          String(
            delivery.customer_name || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            delivery.customer_phone || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            delivery.invoice_number || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            delivery.delivery_address || '',
          )
            .toLowerCase()
            .includes(query),
      )
    }, [deliveries, search])

  return {
    businesses,
    businessId,
    setBusinessId,
    deliveries,
    setDeliveries,
    sales,
    setSales,
    members,
    search,
    setSearch,
    status,
    setStatus,
    loading,
    error,
    setError,
    availableSales,
    filteredDeliveries,
  }
}

export default useDeliveryWorkspace
