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
  const {
    isAuthenticated,
    user,
  } = useAuth()

  const [businesses, setBusinesses] =
    useState([])

  const [business, setBusiness] =
    useState(null)

  const [subscription, setSubscription] =
    useState(getStoredSubscription)

  const [loadedUserKey, setLoadedUserKey] =
    useState('')

  const [loading, setLoading] =
    useState(isAuthenticated)

  const userKey = isAuthenticated
    ? String(user?.id || user?.email || '')
    : ''

  useEffect(() => {
    if (!isAuthenticated) {
      sessionStorage.removeItem(
        'stockpilot-business',
      )

      sessionStorage.removeItem(
        'stockpilot-subscription',
      )

      return undefined
    }

    let mounted = true

    sessionStorage.removeItem(
      'stockpilot-business',
    )

    sessionStorage.removeItem(
      'stockpilot-subscription',
    )

    async function loadBusinesses() {
      try {
        setLoading(true)

        sessionStorage.removeItem(
          'stockpilot-business',
        )

        const businessData =
          await getBusinesses()

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

        setLoadedUserKey(userKey)
      } catch {
        if (!mounted) {
          return
        }

        setBusinesses([])
        setBusiness(null)
        setLoadedUserKey('')

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
  }, [
    isAuthenticated,
    userKey,
  ])

  const selectBusiness = useCallback(
    (businessId) => {
      const selectedBusiness =
        businesses.find(
          (item) =>
            Number(item.id) ===
            Number(businessId),
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

  const updateBusiness = useCallback(
    (updatedBusiness) => {
      setBusinesses((current) =>
        current.map((item) =>
          Number(item.id) ===
          Number(updatedBusiness.id)
            ? updatedBusiness
            : item,
        ),
      )

      setBusiness((current) =>
        current &&
        Number(current.id) ===
          Number(updatedBusiness.id)
          ? updatedBusiness
          : current,
      )

      sessionStorage.setItem(
        'stockpilot-business',
        JSON.stringify(updatedBusiness),
      )
    },
    [],
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

  const userDataReady =
    isAuthenticated &&
    loadedUserKey === userKey

  const value = useMemo(
    () => ({
      businesses: userDataReady
        ? businesses
        : [],

      business: userDataReady
        ? business
        : null,

      businessId: userDataReady
        ? business?.id || null
        : null,

      subscription: userDataReady
        ? subscription
        : null,

      plan: userDataReady
        ? plan
        : null,

      isTrialing: userDataReady
        ? isTrialing
        : false,

      isSubscriptionActive:
        userDataReady
          ? isSubscriptionActive
          : false,

      trialDaysRemaining:
        userDataReady
          ? trialDaysRemaining
          : 0,

      loading: isAuthenticated
        ? loading || !userDataReady
        : false,

      selectBusiness,
      updateBusiness,
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
      userDataReady,
      selectBusiness,
      updateBusiness,
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
