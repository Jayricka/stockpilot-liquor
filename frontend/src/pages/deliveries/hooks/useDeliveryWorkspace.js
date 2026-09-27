import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import { useBusiness } from '../../../context/BusinessContext'

import {
  getBusinessMembers,
  getDeliveries,
} from '../../../services/deliveries'

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
  const {
    businesses,
    businessId,
    selectBusiness,
    loading: businessLoading,
  } = useBusiness()

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
    let active = true

    async function loadWorkspace() {
      if (!businessId) {
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

        if (!active) {
          return
        }

        setDeliveries(deliveryData)
        setSales(salesData)
        setMembers(memberData)
      } catch (err) {
        if (!active) {
          return
        }

        setError(
          getErrorMessage(
            err,
            'Failed to load deliveries.',
          ),
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

  function handleBusinessChange(event) {
    selectBusiness(event.target.value)
  }

  return {
    businesses,
    businessId,
    selectBusiness: handleBusinessChange,
    deliveries,
    setDeliveries,
    sales,
    setSales,
    members,
    search,
    setSearch,
    status,
    setStatus,
    loading:
      businessLoading || loading,
    error,
    setError,
    availableSales,
    filteredDeliveries,
  }
}

export default useDeliveryWorkspace
