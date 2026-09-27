import { useState } from 'react'

import {
  cancelPurchase,
  completePurchase,
  createPurchase,
} from '../../../services/purchases'

export function usePurchaseActions({
  businessId,
  form,
  setPurchases,
  setError,
  closeModal,
}) {
  const [saving, setSaving] =
    useState(false)

  const [actionLoading, setActionLoading] =
    useState(false)

  async function handleSubmit(event) {
    event.preventDefault()

    if (!businessId) {
      setError('Select a business first.')
      return
    }

    if (!form.supplier) {
      setError('Select a supplier.')
      return
    }

    if (!form.reference_number.trim()) {
      setError(
        'Reference number is required.',
      )
      return
    }

    if (!form.items.length) {
      setError(
        'Add at least one product.',
      )
      return
    }

    const invalidItem =
      form.items.some(
        (item) =>
          !item.product ||
          Number(item.quantity) <= 0 ||
          Number(item.unit_cost) < 0,
      )

    if (invalidItem) {
      setError(
        'Complete every product line with valid quantity and cost.',
      )
      return
    }

    try {
      setSaving(true)
      setError('')

      const payload = {
        supplier: Number(form.supplier),
        reference_number:
          form.reference_number.trim(),
        purchase_date:
          form.purchase_date,
        notes: form.notes.trim(),
        items: form.items.map((item) => ({
          product: Number(item.product),
          quantity: item.quantity,
          unit_cost: item.unit_cost,
        })),
      }

      const created =
        await createPurchase(
          businessId,
          payload,
        )

      setPurchases((current) => [
        created,
        ...current,
      ])

      closeModal(true)
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to create purchase.',
      )
    } finally {
      setSaving(false)
    }
  }

  async function handleComplete(
    purchase,
  ) {
    if (
      !window.confirm(
        `Receive stock for ${purchase.reference_number}?`,
      )
    ) {
      return
    }

    try {
      setActionLoading(true)
      setError('')

      const updated =
        await completePurchase(
          businessId,
          purchase.id,
        )

      setPurchases((current) =>
        current.map((item) =>
          item.id === purchase.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to complete purchase.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  async function handleCancel(purchase) {
    if (
      !window.confirm(
        `Cancel purchase ${purchase.reference_number}?`,
      )
    ) {
      return
    }

    try {
      setActionLoading(true)
      setError('')

      const updated =
        await cancelPurchase(
          businessId,
          purchase.id,
        )

      setPurchases((current) =>
        current.map((item) =>
          item.id === purchase.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to cancel purchase.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  return {
    saving,
    actionLoading,
    handleSubmit,
    handleComplete,
    handleCancel,
  }
}
