/* eslint-disable react-refresh/only-export-components */

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useRef,
  useState,
} from 'react'

import { useAuth } from './AuthContext.jsx'

import { getBusinesses } from '../services/dashboard'
import { getCurrentSubscription } from '../services/billing'

const BusinessContext = createContext(null)

function getStoredSubscription() {
  const storedSubscription = sessionStorage.getItem(
    'stocksafi-subscription',
  )

  if (!storedSubscription) return null

  try {
    return JSON.parse(storedSubscription)
  } catch {
    sessionStorage.removeItem('stocksafi-subscription')
    return null
  }
}

export function BusinessProvider({ children }) {
  const { accessToken, isAuthenticated, user } = useAuth()

  const [businesses, setBusinesses] = useState([])
  const [business, setBusiness] = useState(null)
  const [subscription, setSubscription] = useState(
    getStoredSubscription,
  )
  const [loadedUserKey, setLoadedUserKey] = useState('')
  const [loading, setLoading] = useState(isAuthenticated)

  const requestIdRef = useRef(0)
  const selectedBusinessIdRef = useRef(null)

  const userKey = isAuthenticated
    ? `${accessToken}:${user?.id || user?.email || ''}`
    : ''

  const loadBusinessData = useCallback(
    async ({ throwOnError = false, initial = false } = {}) => {
      const requestId = ++requestIdRef.current
      const isCurrentRequest = () =>
        requestId === requestIdRef.current

      if (!initial) {
        setLoading(true)
      }

      try {
        const businessData = await getBusinesses()

        if (!isCurrentRequest()) return

        const currentBusinessId =
          selectedBusinessIdRef.current

        const currentBusiness =
          businessData.find(
            (item) =>
              Number(item.id) ===
              Number(currentBusinessId),
          ) ||
          businessData[0] ||
          null

        selectedBusinessIdRef.current =
          currentBusiness?.id ?? null

        setBusinesses(businessData)
        setBusiness(currentBusiness)

        if (!currentBusiness) {
          setSubscription(null)
          setLoadedUserKey(userKey)

          sessionStorage.removeItem('stocksafi-business')
          sessionStorage.removeItem(
            'stocksafi-subscription',
          )

          return
        }

        sessionStorage.setItem(
          'stocksafi-business',
          JSON.stringify(currentBusiness),
        )

        try {
          const subscriptionData =
            await getCurrentSubscription(currentBusiness.id)

          if (!isCurrentRequest()) return

          setSubscription(subscriptionData)

          sessionStorage.setItem(
            'stocksafi-subscription',
            JSON.stringify(subscriptionData),
          )
        } catch {
          if (!isCurrentRequest()) return

          setSubscription(getStoredSubscription())
        }

        setLoadedUserKey(userKey)
      } catch (error) {
        if (!isCurrentRequest()) return

        selectedBusinessIdRef.current = null

        setBusinesses([])
        setBusiness(null)
        setSubscription(null)
        setLoadedUserKey('')

        sessionStorage.removeItem('stocksafi-business')
        sessionStorage.removeItem(
          'stocksafi-subscription',
        )

        if (throwOnError) throw error
      } finally {
        if (isCurrentRequest()) {
          setLoading(false)
        }
      }
    },
    [userKey],
  )

  useEffect(() => {
    if (!isAuthenticated) {
      requestIdRef.current += 1
      selectedBusinessIdRef.current = null
      return undefined
    }

    let cancelled = false

    Promise.resolve().then(() => {
      if (!cancelled) {
        return loadBusinessData({ initial: true })
      }

      return undefined
    })

    return () => {
      cancelled = true
      requestIdRef.current += 1
    }
  }, [isAuthenticated, loadBusinessData])

  const refreshBusinesses = useCallback(async () => {
    if (!isAuthenticated) {
      throw new Error(
        'You must be signed in to refresh business access.',
      )
    }

    await loadBusinessData({ throwOnError: true })
  }, [isAuthenticated, loadBusinessData])

  const selectBusiness = useCallback(
    (businessId) => {
      const selectedBusiness =
        businesses.find(
          (item) =>
            Number(item.id) === Number(businessId),
        ) || null

      selectedBusinessIdRef.current =
        selectedBusiness?.id ?? null

      setBusiness(selectedBusiness)

      if (selectedBusiness) {
        sessionStorage.setItem(
          'stocksafi-business',
          JSON.stringify(selectedBusiness),
        )
      } else {
        sessionStorage.removeItem('stocksafi-business')
      }
    },
    [businesses],
  )

  const updateBusiness = useCallback((updatedBusiness) => {
    setBusinesses((current) =>
      current.map((item) =>
        Number(item.id) === Number(updatedBusiness.id)
          ? updatedBusiness
          : item,
      ),
    )

    setBusiness((current) => {
      if (
        current &&
        Number(current.id) === Number(updatedBusiness.id)
      ) {
        selectedBusinessIdRef.current = updatedBusiness.id
        return updatedBusiness
      }

      return current
    })

    sessionStorage.setItem(
      'stocksafi-business',
      JSON.stringify(updatedBusiness),
    )
  }, [])

  const plan = subscription?.plan || null

  const isTrialing =
    subscription?.status === 'TRIALING' &&
    subscription?.trial_active === true

  const isSubscriptionActive =
    subscription?.status === 'ACTIVE' || isTrialing

  const trialDaysRemaining =
    subscription?.trial_days_remaining || 0

  const userDataReady =
    isAuthenticated && loadedUserKey === userKey

  const value = useMemo(
    () => ({
      businesses: userDataReady ? businesses : [],
      business: userDataReady ? business : null,
      businessId: userDataReady
        ? business?.id || null
        : null,
      subscription: userDataReady ? subscription : null,
      plan: userDataReady ? plan : null,
      isTrialing: userDataReady ? isTrialing : false,
      isSubscriptionActive: userDataReady
        ? isSubscriptionActive
        : false,
      trialDaysRemaining: userDataReady
        ? trialDaysRemaining
        : 0,
      loading: isAuthenticated
        ? loading || !userDataReady
        : false,
      refreshBusinesses,
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
      refreshBusinesses,
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
      'useBusiness must be used within a BusinessProvider',
    )
  }

  return context
}
