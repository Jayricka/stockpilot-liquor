import { useState } from 'react'

import SupplierFilters from '../../components/suppliers/SupplierFilters'
import SupplierForm from '../../components/suppliers/SupplierForm'
import SupplierHeader from '../../components/suppliers/SupplierHeader'
import SupplierLoading from '../../components/suppliers/SupplierLoading'
import SupplierTable from '../../components/suppliers/SupplierTable'

import { useSupplierActions } from './hooks/useSupplierActions'
import { useSupplierForm } from './hooks/useSupplierForm'
import { useSupplierWorkspace } from './hooks/useSupplierWorkspace'

function Suppliers() {
  const [error, setError] =
    useState('')

  const workspace =
    useSupplierWorkspace({
      setError,
    })

  const form =
    useSupplierForm({
      businessId: workspace.businessId,
      setSuppliers: workspace.setSuppliers,
      setError,
    })

  const actions =
    useSupplierActions({
      businessId: workspace.businessId,
      setSuppliers: workspace.setSuppliers,
      setError,
    })

  return (
    <section className="suppliers-page">
      <SupplierHeader
        businesses={workspace.businesses}
        businessId={workspace.businessId}
        onBusinessChange={
          workspace.handleBusinessChange
        }
        onAdd={form.openCreateModal}
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
          count={
            workspace.filteredSuppliers.length
          }
          search={workspace.search}
          onSearch={
            workspace.handleSearchChange
          }
        />

        <SupplierLoading
          loading={workspace.loading}
          hasSuppliers={
            workspace.filteredSuppliers.length > 0
          }
          searching={Boolean(
            workspace.search.trim(),
          )}
        />

        {!workspace.loading &&
          workspace.filteredSuppliers.length > 0 && (
            <SupplierTable
              suppliers={
                workspace.filteredSuppliers
              }
              onEdit={form.openEditModal}
              onDelete={actions.handleDelete}
            />
          )}
      </div>

      {form.modalOpen && (
        <SupplierForm
          form={form.form}
          editingSupplier={form.editingSupplier}
          saving={form.saving}
          onChange={form.handleChange}
          onSubmit={form.handleSubmit}
          onClose={form.closeModal}
        />
      )}
    </section>
  )
}

export default Suppliers
