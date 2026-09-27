import {
  useCallback,
  useEffect,
  useState,
} from 'react'

import { useBusiness } from '../../../context/BusinessContext'
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
  const {
    businesses,
    business,
    businessId: contextBusinessId,
    selectBusiness,
    loading: businessLoading,
  } = useBusiness()

  const businessId = contextBusinessId
    ? String(contextBusinessId)
    : ''

  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadProducts = useCallback(
    async (selectedBusinessId) => {
      if (!selectedBusinessId) {
        return
      }

      try {
        setLoading(true)
        setError('')

        const data = await getProducts(
          selectedBusinessId,
        )

        const list = normalizeList(data)

        setProducts(
          list.filter(
            (product) => product.is_active,
          ),
        )
      } catch (requestError) {
        setProducts([])
        setError(
          getErrorMessage(requestError),
        )
      } finally {
        setLoading(false)
      }
    },
    [],
  )

  useEffect(() => {
    let active = true

    async function loadWorkspace() {
      if (!businessId) {
        return
      }

      try {
        setLoading(true)
        setError('')

        const data = await getProducts(
          businessId,
        )

        if (!active) {
          return
        }

        const list = normalizeList(data)

        setProducts(
          list.filter(
            (product) => product.is_active,
          ),
        )
      } catch (requestError) {
        if (!active) {
          return
        }

        setProducts([])
        setError(
          getErrorMessage(requestError),
        )
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadWorkspace()

    return () => {
      active = false
    }
  }, [businessId])

  function handleBusinessChange(event) {
    selectBusiness(event.target.value)
  }

  function handleSaleCompleted() {
    loadProducts(businessId)
  }

  return {
    businesses,
    businessId,
    products,
    loading:
      businessLoading || loading,
    error,
    business,
    handleBusinessChange,
    handleSaleCompleted,
  }
}
