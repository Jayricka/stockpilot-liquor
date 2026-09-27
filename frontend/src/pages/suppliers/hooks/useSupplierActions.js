import { deleteSupplier } from '../../../services/suppliers'

export function useSupplierActions({
  businessId,
  setSuppliers,
  setError,
}) {
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

  return {
    handleDelete,
  }
}
