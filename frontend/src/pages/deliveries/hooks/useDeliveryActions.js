import { useState } from 'react'

import {
  assignDelivery,
  cancelDelivery,
  completeDelivery,
  startDelivery,
} from '../../../services/deliveries'

function useDeliveryActions({
  businessId,
  setDeliveries,
  setError,
}) {
  const [actionLoading, setActionLoading] =
    useState(false)

  async function handleAssign(
    delivery,
    userId,
  ) {
    if (!userId) {
      return
    }

    try {
      setActionLoading(true)
      setError('')

      const updated =
        await assignDelivery(
          businessId,
          delivery.id,
          Number(userId),
        )

      setDeliveries((current) =>
        current.map((item) =>
          item.id === delivery.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to assign delivery.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  async function handleStart(delivery) {
    try {
      setActionLoading(true)
      setError('')

      const updated =
        await startDelivery(
          businessId,
          delivery.id,
        )

      setDeliveries((current) =>
        current.map((item) =>
          item.id === delivery.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to start delivery.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  async function handleComplete(
    delivery,
  ) {
    try {
      setActionLoading(true)
      setError('')

      const updated =
        await completeDelivery(
          businessId,
          delivery.id,
        )

      setDeliveries((current) =>
        current.map((item) =>
          item.id === delivery.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to complete delivery.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  async function handleCancel(delivery) {
    if (
      !window.confirm(
        `Cancel delivery for ${delivery.customer_name}?`,
      )
    ) {
      return
    }

    try {
      setActionLoading(true)
      setError('')

      const updated =
        await cancelDelivery(
          businessId,
          delivery.id,
        )

      setDeliveries((current) =>
        current.map((item) =>
          item.id === delivery.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to cancel delivery.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  return {
    actionLoading,
    handleAssign,
    handleStart,
    handleComplete,
    handleCancel,
  }
}

export default useDeliveryActions
