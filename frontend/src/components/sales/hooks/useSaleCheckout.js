import { useMemo, useState } from 'react'

function useSaleCheckout(cart) {
  const [discount, setDiscount] =
    useState('')

  const [paymentMethod, setPaymentMethod] =
    useState('CASH')

  const [amountReceived, setAmountReceived] =
    useState('')

  const subtotal = useMemo(
    () =>
      cart.reduce(
        (total, item) =>
          total +
          Number(item.selling_price || 0) *
            Number(item.quantity || 0),
        0,
      ),
    [cart],
  )

  const discountAmount =
    Number(discount || 0)

  const total = Math.max(
    subtotal - discountAmount,
    0,
  )

  const change =
    paymentMethod === 'CASH'
      ? Math.max(
          Number(amountReceived || 0) -
            total,
          0,
        )
      : 0

  return {
    discount,
    setDiscount,
    paymentMethod,
    setPaymentMethod,
    amountReceived,
    setAmountReceived,
    subtotal,
    discountAmount,
    total,
    change,
  }
}

export default useSaleCheckout
