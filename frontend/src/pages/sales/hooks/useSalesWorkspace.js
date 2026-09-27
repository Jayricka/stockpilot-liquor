import {
  useCallback,
  useEffect,
  useState,
} from 'react'

import { getBusinesses } from '../../../services/dashboard'
import { getProducts } from '../../../services/products'

function normalizeList(data) {
  if (Array.isArray(data)) {
    return data
  }

  return data?.results || []
}

function getErrorMessage(error) {
  const data = error?.response?.data

  if (!data) {
    return 'Something went wrong. Please try again.'
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

  return 'Something went wrong. Please try again.'
}

export function useSalesWorkspace() {
  const [businesses, setBusinesses] = useState([])
  const [businessId, setBusinessId] = useState('')
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadBusinesses = useCallback(async () => {
    try {
      setError('')

      const data = await getBusinesses()
      const list = normalizeList(data)

      setBusinesses(list)

      if (list.length && !businessId) {
        setBusinessId(String(list[0].id))
      }
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }, [businessId])

  const loadProducts = useCallback(async (selectedBusinessId) => {
    if (!selectedBusinessId) {
      setProducts([])
      setLoading(false)
      return
    }

    try {
      setLoading(true)
      setError('')

      const data = await getProducts(selectedBusinessId)
      const list = normalizeList(data)

      setProducts(
        list.filter((product) => product.is_active),
      )
    } catch (requestError) {
      setProducts([])
      setError(getErrorMessage(requestError))
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    const timer = setTimeout(() => {
      loadBusinesses()
    }, 0)

    return () => clearTimeout(timer)
  }, [loadBusinesses])

  useEffect(() => {
    const timer = setTimeout(() => {
      loadProducts(businessId)
    }, 0)

    return () => clearTimeout(timer)
  }, [businessId, loadProducts])

  function handleBusinessChange(event) {
    setBusinessId(event.target.value)
  }

  function handleSaleCompleted() {
    loadProducts(businessId)
  }

  const business = businesses.find(
    (item) => String(item.id) === String(businessId),
  )

  return {
    businesses,
    businessId,
    products,
    loading,
    error,
    business,
    handleBusinessChange,
    handleSaleCompleted,
  }
}
