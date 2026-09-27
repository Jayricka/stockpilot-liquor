import { useState } from 'react'

import {
  createCategory,
} from '../../../services/products'

export function useCategoryForm({
  businessId,
  loadWorkspaceData,
  setError,
}) {
  const [saving, setSaving] = useState(false)
  const [formOpen, setFormOpen] = useState(false)

  function openForm() {
    setFormOpen(true)
    setError('')
  }

  function closeForm() {
    if (saving) {
      return
    }

    setFormOpen(false)
  }

  async function handleSubmit(payload) {
    if (!businessId) {
      setError('Please select a business first.')
      return
    }

    try {
      setSaving(true)
      setError('')

      await createCategory(
        businessId,
        payload,
      )

      await loadWorkspaceData(businessId)

      setFormOpen(false)
    } catch (requestError) {
      const data = requestError?.response?.data

      if (!data) {
        setError(
          'Something went wrong. Please try again.',
        )
        return
      }

      if (typeof data.detail === 'string') {
        setError(data.detail)
        return
      }

      const firstError = Object.values(data)[0]

      if (Array.isArray(firstError)) {
        setError(firstError.join(', '))
      } else if (typeof firstError === 'string') {
        setError(firstError)
      } else {
        setError(
          'Unable to create category. Please check the form.',
        )
      }
    } finally {
      setSaving(false)
    }
  }

  return {
    saving,
    formOpen,
    openForm,
    closeForm,
    handleSubmit,
  }
}
