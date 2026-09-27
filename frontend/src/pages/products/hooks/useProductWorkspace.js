/* eslint-disable react-hooks/set-state-in-effect */
import {
  useCallback,
  useEffect,
  useState,
} from 'react'

import {
  getCategories,
  getProducts,
} from '../../../services/products'

import { useBusiness } from '../../../context/BusinessContext'

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

function normalizeList(data) {
  if (Array.isArray(data)) {
    return data
  }

  return data?.results || []
}

export function useProductWorkspace() {
  const {
    businesses,
    businessId: currentBusinessId,
    selectBusiness,
    loading: businessLoading,
  } = useBusiness()

  const businessId = currentBusinessId
    ? String(currentBusinessId)
    : ''

  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadWorkspaceData = useCallback(
    async (selectedBusinessId) => {
      if (!selectedBusinessId) {
        setProducts([])
        setCategories([])
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const [
          productsData,
          categoriesData,
        ] = await Promise.all([
          getProducts(selectedBusinessId),
          getCategories(selectedBusinessId),
        ])

        setProducts(normalizeList(productsData))
        setCategories(normalizeList(categoriesData))
      } catch (requestError) {
        setProducts([])
        setCategories([])
        setError(getErrorMessage(requestError))
      } finally {
        setLoading(false)
      }
    },
    [],
  )

  useEffect(() => {
    loadWorkspaceData(businessId)
  }, [businessId, loadWorkspaceData])

  function handleBusinessChange(value, resetFilters) {
    selectBusiness(Number(value))
    resetFilters()
  }

  return {
    businesses,
    businessId,
    businessLoading,
    products,
    categories,
    loading,
    error,
    setError,
    selectBusiness,
    loadWorkspaceData,
    handleBusinessChange,
  }
}
