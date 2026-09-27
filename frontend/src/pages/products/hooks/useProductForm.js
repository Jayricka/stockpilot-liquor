import { useState } from 'react'

import {
  createProduct,
  updateProduct,
} from '../../../services/products'

export function useProductForm({
  businessId,
  loadWorkspaceData,
  setError,
}) {
  const [saving, setSaving] = useState(false)
  const [formOpen, setFormOpen] = useState(false)
  const [editingProduct, setEditingProduct] =
    useState(null)

  function openCreateForm() {
    setEditingProduct(null)
    setFormOpen(true)
    setError('')
  }

  function openEditForm(product) {
    setEditingProduct(product)
    setFormOpen(true)
    setError('')
  }

  function closeForm() {
    if (saving) {
      return
    }

    setFormOpen(false)
    setEditingProduct(null)
  }

  async function handleSubmit(payload) {
    if (!businessId) {
      setError('Please select a business first.')
      return
    }

    try {
      setSaving(true)
      setError('')

      if (editingProduct) {
        await updateProduct(
          businessId,
          editingProduct.id,
          payload,
        )
      } else {
        await createProduct(
          businessId,
          payload,
        )
      }

      await loadWorkspaceData(businessId)

      setFormOpen(false)
      setEditingProduct(null)
    } catch (requestError) {
      const data = requestError?.response?.data

      if (!data) {
        setError(
          'Something went wrong. Please try again.',
        )
      } else if (typeof data.detail === 'string') {
        setError(data.detail)
      } else if (Array.isArray(data.detail)) {
        setError(data.detail.join(', '))
      } else if (
        Array.isArray(data.non_field_errors)
      ) {
        setError(
          data.non_field_errors.join(', '),
        )
      } else {
        const firstError = Object.values(data)[0]

        if (Array.isArray(firstError)) {
          setError(firstError.join(', '))
        } else if (typeof firstError === 'string') {
          setError(firstError)
        } else {
          setError(
            'Something went wrong. Please try again.',
          )
        }
      }
    } finally {
      setSaving(false)
    }
  }

  return {
    saving,
    formOpen,
    editingProduct,
    openCreateForm,
    openEditForm,
    closeForm,
    handleSubmit,
  }
}
