import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import {
  cancelPurchase,
  completePurchase,
  createPurchase,
  getPurchases,
} from '../../services/purchases'

import { getBusinesses } from '../../services/dashboard'
import { getProducts } from '../../services/products'
import { getSuppliers } from '../../services/suppliers'

import PurchaseFilters from '../../components/purchases/PurchaseFilters'
import PurchaseForm from '../../components/purchases/PurchaseForm'
import PurchaseHeader from '../../components/purchases/PurchaseHeader'
import PurchaseLoading from '../../components/purchases/PurchaseLoading'
import PurchaseTable from '../../components/purchases/PurchaseTable'

function getToday() {
  return new Date()
    .toISOString()
    .split('T')[0]
}

const emptyItem = {
  product: '',
  quantity: '',
  unit_cost: '',
}

const emptyForm = {
  supplier: '',
  reference_number: '',
  purchase_date: getToday(),
  notes: '',
  items: [{ ...emptyItem }],
}

function Purchases() {
  const [businesses, setBusinesses] =
    useState([])

  const [businessId, setBusinessId] =
    useState('')

  const [purchases, setPurchases] =
    useState([])

  const [suppliers, setSuppliers] =
    useState([])

  const [products, setProducts] =
    useState([])

  const [search, setSearch] =
    useState('')

  const [status, setStatus] =
    useState('')

  const [loading, setLoading] =
    useState(true)

  const [saving, setSaving] =
    useState(false)

  const [actionLoading, setActionLoading] =
    useState(false)

  const [error, setError] =
    useState('')

  const [modalOpen, setModalOpen] =
    useState(false)

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
    async function loadWorkspace() {
      if (!businessId) {
        setPurchases([])
        setSuppliers([])
        setProducts([])
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const [
          purchaseData,
          supplierData,
          productData,
        ] = await Promise.all([
          getPurchases(
            businessId,
            status,
          ),
          getSuppliers(businessId),
          getProducts(businessId),
        ])

        setPurchases(purchaseData)
        setSuppliers(supplierData)
        setProducts(productData)
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Failed to load purchases.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadWorkspace()
  }, [businessId, status])

  const filteredPurchases =
    useMemo(() => {
      const query =
        search.trim().toLowerCase()

      if (!query) {
        return purchases
      }

      return purchases.filter(
        (purchase) =>
          String(
            purchase.reference_number || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            purchase.supplier_name || '',
          )
            .toLowerCase()
            .includes(query),
      )
    }, [purchases, search])

  function openCreateModal() {
    setForm({
      ...emptyForm,
      purchase_date: getToday(),
      items: [{ ...emptyItem }],
    })

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

  function handleItemChange(
    index,
    field,
    value,
  ) {
    setForm((current) => ({
      ...current,
      items: current.items.map(
        (item, itemIndex) =>
          itemIndex === index
            ? {
                ...item,
                [field]: value,
              }
            : item,
      ),
    }))
  }

  function addItem() {
    setForm((current) => ({
      ...current,
      items: [
        ...current.items,
        { ...emptyItem },
      ],
    }))
  }

  function removeItem(index) {
    setForm((current) => ({
      ...current,
      items: current.items.filter(
        (_, itemIndex) =>
          itemIndex !== index,
      ),
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

    if (!form.supplier) {
      setError('Select a supplier.')
      return
    }

    if (!form.reference_number.trim()) {
      setError(
        'Reference number is required.',
      )
      return
    }

    if (!form.items.length) {
      setError(
        'Add at least one product.',
      )
      return
    }

    const invalidItem =
      form.items.some(
        (item) =>
          !item.product ||
          Number(item.quantity) <= 0 ||
          Number(item.unit_cost) < 0,
      )

    if (invalidItem) {
      setError(
        'Complete every product line with valid quantity and cost.',
      )
      return
    }

    try {
      setSaving(true)
      setError('')

      const payload = {
        supplier: Number(form.supplier),
        reference_number:
          form.reference_number.trim(),
        purchase_date:
          form.purchase_date,
        notes: form.notes.trim(),
        items: form.items.map((item) => ({
          product: Number(item.product),
          quantity: item.quantity,
          unit_cost: item.unit_cost,
        })),
      }

      const created =
        await createPurchase(
          businessId,
          payload,
        )

      setPurchases((current) => [
        created,
        ...current,
      ])

      closeModal(true)
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to create purchase.',
      )
    } finally {
      setSaving(false)
    }
  }

  async function handleComplete(
    purchase,
  ) {
    if (
      !window.confirm(
        `Receive stock for ${purchase.reference_number}?`,
      )
    ) {
      return
    }

    try {
      setActionLoading(true)
      setError('')

      const updated =
        await completePurchase(
          businessId,
          purchase.id,
        )

      setPurchases((current) =>
        current.map((item) =>
          item.id === purchase.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to complete purchase.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  async function handleCancel(purchase) {
    if (
      !window.confirm(
        `Cancel purchase ${purchase.reference_number}?`,
      )
    ) {
      return
    }

    try {
      setActionLoading(true)
      setError('')

      const updated =
        await cancelPurchase(
          businessId,
          purchase.id,
        )

      setPurchases((current) =>
        current.map((item) =>
          item.id === purchase.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to cancel purchase.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  return (
    <section className="purchases-page">
      <PurchaseHeader
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
          className="purchases-error"
          role="alert"
        >
          {error}
        </div>
      )}

      <div className="purchases-card">
        <PurchaseFilters
          count={filteredPurchases.length}
          search={search}
          status={status}
          onSearch={(event) =>
            setSearch(
              event.target.value,
            )
          }
          onStatusChange={(event) =>
            setStatus(
              event.target.value,
            )
          }
        />

        <PurchaseLoading
          loading={loading}
          hasPurchases={
            filteredPurchases.length > 0
          }
          searching={Boolean(search.trim())}
        />

        {!loading &&
          filteredPurchases.length > 0 && (
            <PurchaseTable
              purchases={
                filteredPurchases
              }
              actionLoading={
                actionLoading
              }
              onComplete={
                handleComplete
              }
              onCancel={handleCancel}
            />
          )}
      </div>

      {modalOpen && (
        <PurchaseForm
          suppliers={suppliers}
          products={products}
          form={form}
          saving={saving}
          onChange={handleChange}
          onItemChange={
            handleItemChange
          }
          onAddItem={addItem}
          onRemoveItem={removeItem}
          onSubmit={handleSubmit}
          onClose={closeModal}
        />
      )}
    </section>
  )
}

export default Purchases
