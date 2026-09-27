import { useState } from 'react'

import PurchaseFilters from '../../components/purchases/PurchaseFilters'
import PurchaseForm from '../../components/purchases/PurchaseForm'
import PurchaseHeader from '../../components/purchases/PurchaseHeader'
import PurchaseLoading from '../../components/purchases/PurchaseLoading'
import PurchaseTable from '../../components/purchases/PurchaseTable'

import { usePurchaseActions } from '../../components/purchases/hooks/usePurchaseActions'
import { usePurchaseForm } from '../../components/purchases/hooks/usePurchaseForm'
import { usePurchaseWorkspace } from '../../components/purchases/hooks/usePurchaseWorkspace'

function Purchases() {
  const [status, setStatus] =
    useState('')

  const [modalOpen, setModalOpen] =
    useState(false)

  const {
    businesses,
    businessId,
    setBusinessId,
    suppliers,
    products,
    search,
    setSearch,
    loading,
    error,
    setError,
    filteredPurchases,
    setPurchases,
  } = usePurchaseWorkspace(status)

  const {
    form,
    resetForm,
    handleChange,
    handleItemChange,
    addItem,
    removeItem,
  } = usePurchaseForm()

  function openCreateModal() {
    resetForm()
    setError('')
    setModalOpen(true)
  }

  function closeModal(force = false) {
    if (saving && !force) {
      return
    }

    setModalOpen(false)
    resetForm()
  }

  const {
    saving,
    actionLoading,
    handleSubmit,
    handleComplete,
    handleCancel,
  } = usePurchaseActions({
    businessId,
    form,
    setPurchases,
    setError,
    closeModal,
  })

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
