import DeliveryFilters from '../../components/deliveries/DeliveryFilters'
import DeliveryForm from '../../components/deliveries/DeliveryForm'
import DeliveryHeader from '../../components/deliveries/DeliveryHeader'
import DeliveryLoading from '../../components/deliveries/DeliveryLoading'
import DeliveryTable from '../../components/deliveries/DeliveryTable'

import useDeliveryActions from './hooks/useDeliveryActions'
import useDeliveryForm from './hooks/useDeliveryForm'
import useDeliveryWorkspace from './hooks/useDeliveryWorkspace'

function Deliveries() {
  const {
    businesses,
    businessId,
    selectBusiness,
    setDeliveries,
    setSales,
    members,
    search,
    setSearch,
    status,
    setStatus,
    loading,
    error,
    setError,
    availableSales,
    filteredDeliveries,
  } = useDeliveryWorkspace()

  const {
    saving,
    modalOpen,
    form,
    openCreateModal,
    closeModal,
    handleChange,
    handleSubmit,
  } = useDeliveryForm({
    businessId,
    setDeliveries,
    setSales,
    setError,
  })

  const {
    actionLoading,
    handleAssign,
    handleStart,
    handleComplete,
    handleCancel,
  } = useDeliveryActions({
    businessId,
    setDeliveries,
    setError,
  })


  return (
    <section className="deliveries-page">
      <DeliveryHeader
        businesses={businesses}
        businessId={businessId}
        onBusinessChange={selectBusiness}
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
