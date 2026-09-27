import { useState } from 'react'

import {
  completeSale,
  createSale,
} from '../../../services/sales'

function getErrorMessage(error) {
  const data = error?.response?.data

  if (!data) {
    return 'Unable to complete the sale.'
  }

  if (typeof data.detail === 'string') {
    return data.detail
  }

  if (Array.isArray(data.detail)) {
    return data.detail.join(', ')
  }

  if (Array.isArray(data.non_field_errors)) {
    return data.non_field_errors.join(', ')
  }

  const firstError = Object.values(data)[0]

  if (Array.isArray(firstError)) {
    return firstError.join(', ')
  }

  if (typeof firstError === 'string') {
    return firstError
  }

  return 'Unable to complete the sale.'
}

function getToday() {
  const now = new Date()

  const year = now.getFullYear()
  const month = String(
    now.getMonth() + 1,
  ).padStart(2, '0')

  const day = String(
    now.getDate(),
  ).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function useSaleActions({
  businessId,
  cart,
  discountAmount,
  subtotal,
  paymentMethod,
  amountReceived,
  total,
  clearCart,
  setDiscount,
  setAmountReceived,
  setPaymentMethod,
  onSaleCompleted,
}) {
  const [saving, setSaving] =
    useState(false)

  const [error, setError] =
    useState('')

  async function handleCompleteSale() {
    setError('')

    if (!businessId) {
      setError(
        'Please select a business first.',
      )
      return
    }

    if (!cart.length) {
      setError(
        'Add at least one product to the cart.',
      )
      return
    }

    if (discountAmount < 0) {
      setError(
        'Discount cannot be negative.',
      )
      return
    }

    if (discountAmount > subtotal) {
      setError(
        'Discount cannot exceed the sale subtotal.',
      )
      return
    }

    if (
      paymentMethod === 'CASH' &&
      Number(amountReceived || 0) <
        total
    ) {
      setError(
        'Amount received is insufficient.',
      )
      return
    }

    try {
      setSaving(true)

      const payload = {
        invoice_number: `SP-${Date.now()}`,
        discount_amount:
          discountAmount,
        payment_method:
          paymentMethod,
        sale_date: getToday(),
        items: cart.map((item) => ({
          product: item.id,
          quantity: item.quantity,
        })),
      }

      const sale = await createSale(
        businessId,
        payload,
      )

      await completeSale(
        businessId,
        sale.id,
      )

      clearCart()
      setDiscount('')
      setAmountReceived('')
      setPaymentMethod('CASH')

      if (onSaleCompleted) {
        onSaleCompleted()
      }
    } catch (requestError) {
      setError(
        getErrorMessage(requestError),
      )
    } finally {
      setSaving(false)
    }
  }

  return {
    saving,
    error,
    setError,
    handleCompleteSale,
  }
}

export default useSaleActions
