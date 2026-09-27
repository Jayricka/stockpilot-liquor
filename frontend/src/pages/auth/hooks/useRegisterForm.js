import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { useAuth } from '../../../context/AuthContext.jsx'
import { registerUser } from '../../../services/auth.js'

const validPlans = [
  'starter',
  'growth',
  'business',
]

export function useRegisterForm(requestedPlan) {
  const navigate = useNavigate()
  const { saveSession } = useAuth()

  const selectedPlan = validPlans.includes(
    requestedPlan,
  )
    ? requestedPlan
    : 'starter'

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
  })

  const [confirmPassword, setConfirmPassword] =
    useState('')

  const [showPassword, setShowPassword] =
    useState(false)

  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false)

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  function handleChange(event) {
    const { name, value } = event.target

    setFormData((current) => ({
      ...current,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setError('')

    if (formData.password !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    if (formData.password.length < 8) {
      setError(
        'Password must be at least 8 characters.',
      )
      return
    }

    setLoading(true)

    try {
      const session = await registerUser(formData)

      saveSession(session, session.user)

      navigate(
        `/onboarding?plan=${selectedPlan}`,
        { replace: true },
      )
    } catch (requestError) {
      const responseData =
        requestError.response?.data

      const message =
        responseData?.detail ||
        responseData?.email?.[0] ||
        responseData?.password?.[0] ||
        'Unable to create your account. Please try again.'

      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return {
    selectedPlan,
    formData,
    confirmPassword,
    showPassword,
    showConfirmPassword,
    error,
    loading,
    handleChange,
    handleSubmit,
    setConfirmPassword,
    setShowPassword,
    setShowConfirmPassword,
  }
}
