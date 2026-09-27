import { useState } from 'react'

import { createDelivery } from '../../../services/deliveries'

const emptyForm = {
  sale: '',
  customer_name: '',
  customer_phone: '',
  delivery_address: '',
  delivery_fee: '0',
  notes: '',
}

function useDeliveryForm({
  businessId,
  setDeliveries,
  setSales,
  setError,
}) {
  const [saving, setSaving] =
    useState(false)

  const [modalOpen, setModalOpen] =
    useState(false)

  const [form, setForm] =
    useState(emptyForm)

  function openCreateModal() {
    setForm(emptyForm)
    setError('')
    setModalOpen(true)
  }

  function closeModal(force = false) {
    if (saving && !force) {
      return
    }

    setModalOpen(false)
    setForm(emptyForm)
  }

  function handleChange(event) {
    const {
      name,
      value,
    } = event.target

    setForm((current) => ({
      ...current,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    if (!businessId) {
      setError(
        'Select a business first.',
      )
      return
    }

    if (!form.sale) {
      setError(
        'Select a completed sale.',
      )
      return
    }

    if (!form.customer_name.trim()) {
      setError(
        'Customer name is required.',
      )
      return
    }

    if (!form.customer_phone.trim()) {
      setError(
        'Customer phone is required.',
      )
      return
    }

    if (!form.delivery_address.trim()) {
      setError(
        'Delivery address is required.',
      )
      return
    }

    try {
      setSaving(true)
      setError('')

      const payload = {
        sale: Number(form.sale),
        customer_name:
          form.customer_name.trim(),
        customer_phone:
          form.customer_phone.trim(),
        delivery_address:
          form.delivery_address.trim(),
        delivery_fee:
          form.delivery_fee || '0',
        notes: form.notes.trim(),
      }

      const created =
        await createDelivery(
          businessId,
          payload,
        )

      setDeliveries((current) => [
        created,
        ...current,
      ])

      setSales((current) =>
        current.filter(
          (sale) =>
            sale.id !==
            Number(form.sale),
        ),
      )

      closeModal(true)
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to create delivery.',
      )
    } finally {
      setSaving(false)
    }
  }

  return {
    saving,
    modalOpen,
    form,
    openCreateModal,
    closeModal,
    handleChange,
    handleSubmit,
  }
}

export default useDeliveryForm
