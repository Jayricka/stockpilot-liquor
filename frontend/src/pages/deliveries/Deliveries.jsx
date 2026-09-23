import {
  useEffect,
  useMemo,
  useState,
} from 'react'

import {
  assignDelivery,
  cancelDelivery,
  completeDelivery,
  createDelivery,
  getBusinessMembers,
  getDeliveries,
  startDelivery,
} from '../../services/deliveries'

import { getBusinesses } from '../../services/dashboard'
import { getSales } from '../../services/sales'

import DeliveryFilters from '../../components/deliveries/DeliveryFilters'
import DeliveryForm from '../../components/deliveries/DeliveryForm'
import DeliveryHeader from '../../components/deliveries/DeliveryHeader'
import DeliveryLoading from '../../components/deliveries/DeliveryLoading'
import DeliveryTable from '../../components/deliveries/DeliveryTable'

const emptyForm = {
  sale: '',
  customer_name: '',
  customer_phone: '',
  delivery_address: '',
  delivery_fee: '0',
  notes: '',
}

function Deliveries() {
  const [businesses, setBusinesses] =
    useState([])

  const [businessId, setBusinessId] =
    useState('')

  const [deliveries, setDeliveries] =
    useState([])

  const [sales, setSales] =
    useState([])

  const [members, setMembers] =
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
        setDeliveries([])
        setSales([])
        setMembers([])
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const [
          deliveryData,
          salesData,
          memberData,
        ] = await Promise.all([
          getDeliveries(
            businessId,
            status,
          ),
          getSales(businessId, {
            status: 'COMPLETED',
          }),
          getBusinessMembers(
            businessId,
          ),
        ])

        setDeliveries(deliveryData)
        setSales(salesData)
        setMembers(memberData)
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Failed to load deliveries.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadWorkspace()
  }, [businessId, status])

  const availableSales =
    useMemo(() => {
      const deliverySaleIds =
        new Set(
          deliveries.map(
            (delivery) =>
              Number(delivery.sale),
          ),
        )

      return sales.filter(
        (sale) =>
          !deliverySaleIds.has(
            Number(sale.id),
          ),
      )
    }, [sales, deliveries])

  const filteredDeliveries =
    useMemo(() => {
      const query =
        search.trim().toLowerCase()

      if (!query) {
        return deliveries
      }

      return deliveries.filter(
        (delivery) =>
          String(
            delivery.customer_name || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            delivery.customer_phone || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            delivery.invoice_number || '',
          )
            .toLowerCase()
            .includes(query) ||
          String(
            delivery.delivery_address || '',
          )
            .toLowerCase()
            .includes(query),
      )
    }, [deliveries, search])

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

  async function handleAssign(
    delivery,
    userId,
  ) {
    if (!userId) {
      return
    }

    try {
      setActionLoading(true)
      setError('')

      const updated =
        await assignDelivery(
          businessId,
          delivery.id,
          Number(userId),
        )

      setDeliveries((current) =>
        current.map((item) =>
          item.id === delivery.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to assign delivery.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  async function handleStart(delivery) {
    try {
      setActionLoading(true)
      setError('')

      const updated =
        await startDelivery(
          businessId,
          delivery.id,
        )

      setDeliveries((current) =>
        current.map((item) =>
          item.id === delivery.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to start delivery.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  async function handleComplete(
    delivery,
  ) {
    try {
      setActionLoading(true)
      setError('')

      const updated =
        await completeDelivery(
          businessId,
          delivery.id,
        )

      setDeliveries((current) =>
        current.map((item) =>
          item.id === delivery.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to complete delivery.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  async function handleCancel(delivery) {
    if (
      !window.confirm(
        `Cancel delivery for ${delivery.customer_name}?`,
      )
    ) {
      return
    }

    try {
      setActionLoading(true)
      setError('')

      const updated =
        await cancelDelivery(
          businessId,
          delivery.id,
        )

      setDeliveries((current) =>
        current.map((item) =>
          item.id === delivery.id
            ? updated
            : item,
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Failed to cancel delivery.',
      )
    } finally {
      setActionLoading(false)
    }
  }

  return (
    <section className="deliveries-page">
      <DeliveryHeader
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
          className="deliveries-error"
          role="alert"
        >
          {error}
        </div>
      )}

      <div className="deliveries-card">
        <DeliveryFilters
          count={filteredDeliveries.length}
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

        <DeliveryLoading
          loading={loading}
          hasDeliveries={
            filteredDeliveries.length > 0
          }
          searching={Boolean(search.trim())}
        />

        {!loading &&
          filteredDeliveries.length > 0 && (
            <DeliveryTable
              deliveries={
                filteredDeliveries
              }
              members={members}
              actionLoading={
                actionLoading
              }
              onAssign={handleAssign}
              onStart={handleStart}
              onComplete={
                handleComplete
              }
              onCancel={handleCancel}
            />
          )}
      </div>

      {modalOpen && (
        <DeliveryForm
          sales={availableSales}
          form={form}
          saving={saving}
          onChange={handleChange}
          onSubmit={handleSubmit}
          onClose={closeModal}
        />
      )}
    </section>
  )
}

export default Deliveries
