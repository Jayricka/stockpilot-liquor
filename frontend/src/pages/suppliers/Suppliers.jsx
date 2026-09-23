import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import {
  createSupplier,
  deleteSupplier,
  getSuppliers,
  updateSupplier,
} from '../../services/suppliers'

import { getBusinesses } from '../../services/dashboard'

import SupplierFilters from '../../components/suppliers/SupplierFilters'
import SupplierForm from '../../components/suppliers/SupplierForm'
import SupplierHeader from '../../components/suppliers/SupplierHeader'
import SupplierLoading from '../../components/suppliers/SupplierLoading'
import SupplierTable from '../../components/suppliers/SupplierTable'

const emptyForm = {
  name: '',
  phone: '',
  email: '',
  address: '',
  notes: '',
  is_active: true,
}

function Suppliers() {
  const [businesses, setBusinesses] =
    useState([])

  const [businessId, setBusinessId] =
    useState('')

  const [suppliers, setSuppliers] =
    useState([])

  const [search, setSearch] =
    useState('')

  const [loading, setLoading] =
    useState(true)

  const [saving, setSaving] =
    useState(false)

  const [error, setError] =
    useState('')

  const [modalOpen, setModalOpen] =
    useState(false)

  const [editingSupplier, setEditingSupplier] =
    useState(null)

  const [form, setForm] =
    useState(emptyForm)

  useEffect(() => {
    async function loadBusinesses() {
      try {
        const data =
          await getBusinesses()

        setBusinesses(data)

        if (data.length) {
          setBusinessId(
            String(data[0].id),
          )
        }
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Failed to load businesses.',
        )
      }
    }

    loadBusinesses()
  }, [])

  useEffect(() => {
    async function loadSuppliers() {
      if (!businessId) {
        setSuppliers([])
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const data =
          await getSuppliers(businessId)

        setSuppliers(data)
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Failed to load suppliers.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadSuppliers()
  }, [businessId])

  const filteredSuppliers =
    useMemo(() => {
      const query =
        search.trim().toLowerCase()

      if (!query) {
        return suppliers
      }

      return suppliers.filter(
        (supplier) =>
          String(
            supplier.name || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            supplier.phone || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            supplier.email || '',
          )
            .toLowerCase()
            .includes(query),
      )
    }, [suppliers, search])

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

  async function handleDelete(supplier) {
    if (
      !window.confirm(
        `Delete ${supplier.name}?`,
      )
    ) {
      return
    }

    try {
      setError('')

      await deleteSupplier(
        businessId,
        supplier.id,
      )

      setSuppliers((current) =>
        current.filter(
          (item) =>
            item.id !== supplier.id,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to delete supplier.',
      )
    }
  }

  return (
    <section className="suppliers-page">
      <SupplierHeader
        businesses={businesses}
        businessId={businessId}
        onBusinessChange={(event) =>
          setBusinessId(
            event.target.value,
          )
        }
        onAdd={openCreateModal}
      />

      {error && (
        <div
          className="suppliers-error"
          role="alert"
        >
          {error}
        </div>
      )}

      <div className="suppliers-card">
        <SupplierFilters
          count={filteredSuppliers.length}
          search={search}
          onSearch={(event) =>
            setSearch(event.target.value)
          }
        />

        <SupplierLoading
          loading={loading}
          hasSuppliers={
            filteredSuppliers.length > 0
          }
          searching={Boolean(search.trim())}
        />

        {!loading &&
          filteredSuppliers.length > 0 && (
            <SupplierTable
              suppliers={filteredSuppliers}
              onEdit={openEditModal}
              onDelete={handleDelete}
            />
          )}
      </div>

      {modalOpen && (
        <SupplierForm
          form={form}
          editingSupplier={editingSupplier}
          saving={saving}
          onChange={handleChange}
          onSubmit={handleSubmit}
          onClose={closeModal}
        />
      )}
    </section>
  )
}

export default Suppliers
