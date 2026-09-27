import { useState } from 'react'

import {
  createSupplier,
  updateSupplier,
} from '../../../services/suppliers'

const emptyForm = {
  name: '',
  phone: '',
  email: '',
  address: '',
  notes: '',
  is_active: true,
}

export function useSupplierForm({
  businessId,
  setSuppliers,
  setError,
}) {
  const [saving, setSaving] =
    useState(false)

  const [modalOpen, setModalOpen] =
    useState(false)

  const [editingSupplier, setEditingSupplier] =
    useState(null)

  const [form, setForm] =
    useState(emptyForm)

  function openCreateModal() {
    setEditingSupplier(null)
    setForm(emptyForm)
    setError('')
    setModalOpen(true)
  }

  function openEditModal(supplier) {
    setEditingSupplier(supplier)

    setForm({
      name: supplier.name || '',
      phone: supplier.phone || '',
      email: supplier.email || '',
      address: supplier.address || '',
      notes: supplier.notes || '',
      is_active:
        supplier.is_active ?? true,
    })

    setError('')
    setModalOpen(true)
  }

  function closeModal() {
    if (saving) {
      return
    }

    setModalOpen(false)
    setEditingSupplier(null)
    setForm(emptyForm)
  }

  function handleChange(event) {
    const {
      name,
      value,
      type,
      checked,
    } = event.target

    setForm((current) => ({
      ...current,
      [name]:
        type === 'checkbox'
          ? checked
          : value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    if (!businessId) {
      setError('Select a business first.')
      return
    }

    if (!form.name.trim()) {
      setError('Supplier name is required.')
      return
    }

    try {
      setSaving(true)
      setError('')

      const payload = {
        ...form,
        name: form.name.trim(),
        phone: form.phone.trim(),
        email: form.email.trim(),
        address: form.address.trim(),
        notes: form.notes.trim(),
      }

      if (editingSupplier) {
        const updated =
          await updateSupplier(
            businessId,
            editingSupplier.id,
            payload,
          )

        setSuppliers((current) =>
          current.map((supplier) =>
            supplier.id ===
            editingSupplier.id
              ? updated
              : supplier,
          ),
        )
      } else {
        const created =
          await createSupplier(
            businessId,
            payload,
          )

        setSuppliers((current) => [
          ...current,
          created,
        ])
      }

      closeModal()
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to save supplier.',
      )
    } finally {
      setSaving(false)
    }
  }

  return {
    form,
    saving,
    modalOpen,
    editingSupplier,
    openCreateModal,
    openEditModal,
    closeModal,
    handleChange,
    handleSubmit,
  }
}
