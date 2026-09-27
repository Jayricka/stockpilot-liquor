/* eslint-disable react-refresh/only-export-components */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from 'react'

import { useAuth } from './AuthContext.jsx'

import { getBusinesses } from '../services/dashboard'
import { getCurrentSubscription } from '../services/billing'

const BusinessContext = createContext(null)

function getStoredSubscription() {
  const storedSubscription =
    sessionStorage.getItem(
      'stockpilot-subscription',
    )

  if (!storedSubscription) {
    return null
  }

  try {
    return JSON.parse(storedSubscription)
  } catch {
    sessionStorage.removeItem(
      'stockpilot-subscription',
    )
    return null
  }
}

export function BusinessProvider({ children }) {
  const { isAuthenticated } = useAuth()

  const [businesses, setBusinesses] = useState([])
  const [business, setBusiness] = useState(null)
  const [subscription, setSubscription] = useState(
    getStoredSubscription,
  )
  const [loading, setLoading] = useState(
    isAuthenticated,
  )

  useEffect(() => {
    if (!isAuthenticated) {
      return undefined
    }

    let mounted = true

    async function loadBusinesses() {
      try {
        setLoading(true)

        sessionStorage.removeItem(
          'stockpilot-business',
        )

        const businessData = await getBusinesses()

        if (!mounted) {
          return
        }

        setBusinesses(businessData)

        const currentBusiness =
          businessData[0] || null

        setBusiness(currentBusiness)

        if (currentBusiness) {
          sessionStorage.setItem(
            'stockpilot-business',
            JSON.stringify(currentBusiness),
          )
        }
      } catch {
        if (!mounted) {
          return
        }

        setBusinesses([])
        setBusiness(null)

        sessionStorage.removeItem(
          'stockpilot-business',
        )
      } finally {
        if (mounted) {
          setLoading(false)
        }
      }
    }

    async function loadSubscription() {
      try {
        const subscriptionData =
          await getCurrentSubscription()

        if (!mounted) {
          return
        }

        setSubscription(subscriptionData)

        sessionStorage.setItem(
          'stockpilot-subscription',
          JSON.stringify(subscriptionData),
        )
      } catch {
        if (!mounted) {
          return
        }

        setSubscription(
          getStoredSubscription(),
        )
      }
    }

    loadBusinesses()
    loadSubscription()

    return () => {
      mounted = false
    }
  }, [isAuthenticated])

  const selectBusiness = useCallback(
    (businessId) => {
      const selectedBusiness =
        businesses.find(
          (item) => item.id === businessId,
        ) || null

      setBusiness(selectedBusiness)

      if (selectedBusiness) {
        sessionStorage.setItem(
          'stockpilot-business',
          JSON.stringify(selectedBusiness),
        )
      } else {
        sessionStorage.removeItem(
          'stockpilot-business',
        )
      }
    },
    [businesses],
  )

  const plan = subscription?.plan || null

  const isTrialing =
    subscription?.status === 'TRIALING' &&
    subscription?.trial_active === true

  const isSubscriptionActive =
    subscription?.status === 'ACTIVE' ||
    isTrialing

  const trialDaysRemaining =
    subscription?.trial_days_remaining || 0

  const value = useMemo(
    () => ({
      businesses: isAuthenticated
        ? businesses
        : [],

      business: isAuthenticated
        ? business
        : null,

      businessId: isAuthenticated
        ? business?.id || null
        : null,

      subscription: isAuthenticated
        ? subscription
        : null,

      plan: isAuthenticated
        ? plan
        : null,

      isTrialing: isAuthenticated
        ? isTrialing
        : false,

      isSubscriptionActive:
        isAuthenticated
          ? isSubscriptionActive
          : false,

      trialDaysRemaining:
        isAuthenticated
          ? trialDaysRemaining
          : 0,

      loading: isAuthenticated
        ? loading
        : false,

      selectBusiness,
    }),
    [
      isAuthenticated,
      businesses,
      business,
      subscription,
      plan,
      isTrialing,
      isSubscriptionActive,
      trialDaysRemaining,
      loading,
      selectBusiness,
    ],
  )

  return (
    <BusinessContext.Provider value={value}>
      {children}
    </BusinessContext.Provider>
  )
}

export function useBusiness() {
  const context = useContext(BusinessContext)

  if (!context) {
    throw new Error(
      'useBusiness must be used inside a BusinessProvider',
    )
  }

  return context
}
