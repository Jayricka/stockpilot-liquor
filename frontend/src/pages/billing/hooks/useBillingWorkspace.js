import {
  useEffect,
  useState,
} from 'react'

import { useBusiness } from '../../../context/BusinessContext'
import { getPlans } from '../../../services/billing'

export function useBillingWorkspace() {
  const {
    business,
    subscription,
    loading: businessLoading,
    isTrialing,
    isSubscriptionActive,
    trialDaysRemaining,
  } = useBusiness()

  const [plans, setPlans] = useState([])
  const [plansLoading, setPlansLoading] =
    useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    if (businessLoading || !business) {
      return undefined
    }

    let active = true

    async function loadPlans() {
      try {
        setError('')

        const planData = await getPlans()

        if (!active) {
          return
        }

        setPlans(planData)
      } catch (err) {
        if (!active) {
          return
        }

        setError(
          err.response?.data?.detail ||
            'Unable to load billing plans.',
        )
      } finally {
        if (active) {
          setPlansLoading(false)
        }
      }
    }

    loadPlans()

    return () => {
      active = false
    }
  }, [businessLoading, business])

  return {
    business,
    subscription,
    plans,
    loading:
      businessLoading || plansLoading,
    error,
    isTrialing,
    isSubscriptionActive,
    trialDaysRemaining,
  }
}
