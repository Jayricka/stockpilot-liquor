import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { onboardBusiness } from '../../../services/businesses.js'

const emptyForm = {
  name: '',
  business_type: 'liquor_store',
  phone: '',
  email: '',
  address: '',
  license_number: '',
  plan: 'starter',
}

export function useBusinessOnboarding(
  initialPlan,
) {
  const navigate = useNavigate()

  const [formData, setFormData] =
    useState({
      ...emptyForm,
      plan: initialPlan,
    })

  const [error, setError] =
    useState('')

  const [loading, setLoading] =
    useState(false)

  function handleChange(event) {
    const {
      name,
      value,
    } = event.target

    setFormData((current) => ({
      ...current,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setError('')
    setLoading(true)

    try {
      const response =
        await onboardBusiness(formData)

      sessionStorage.setItem(
        'stockpilot-business',
        JSON.stringify(response.business),
      )

      sessionStorage.setItem(
        'stockpilot-subscription',
        JSON.stringify(
          response.subscription,
        ),
      )

      navigate('/dashboard', {
        replace: true,
      })
    } catch (requestError) {
      const responseData =
        requestError.response?.data

      const message =
        responseData?.detail ||
        responseData?.name?.[0] ||
        responseData?.phone?.[0] ||
        responseData?.plan?.[0] ||
        'Unable to create your business. Please try again.'

      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return {
    formData,
    error,
    loading,
    handleChange,
    handleSubmit,
  }
}
