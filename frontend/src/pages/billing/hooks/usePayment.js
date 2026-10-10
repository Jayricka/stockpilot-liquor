
import {
  useCallback,
  useState,
} from 'react'

import { useBusiness } from '../../../context/BusinessContext'
import { createPayment } from '../../../services/billing'

export function usePayment() {
  const { business } = useBusiness()

  const [payment, setPayment] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const initiatePayment = useCallback(
    async ({ phoneNumber }) => {
      if (!business) {
        setError(
          'No business is currently selected.',
        )
        return null
      }

      try {
        setLoading(true)
        setError('')

        const paymentData = await createPayment(
          business.id,
          {
            phone_number: phoneNumber,
          },
        )

        setPayment(paymentData)

        return paymentData
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Unable to initiate M-Pesa payment.',
        )

        return null
      } finally {
        setLoading(false)
      }
    },
    [business],
  )

  return {
    payment,
    loading,
    error,
    initiatePayment,
  }
}
