import api from './api'

function normalizeList(data) {
  if (Array.isArray(data)) {
    return data
  }

  return data?.results || []
}

export async function getSuppliers(businessId) {
  const response = await api.get(
    `/businesses/${businessId}/suppliers/`,
  )

  return normalizeList(response.data)
}

export async function createSupplier(
  businessId,
  payload,
) {
  const response = await api.post(
    `/businesses/${businessId}/suppliers/`,
    payload,
  )

  return response.data
}

export async function updateSupplier(
  businessId,
  supplierId,
  payload,
) {
  const response = await api.patch(
    `/businesses/${businessId}/suppliers/${supplierId}/`,
    payload,
  )

  return response.data
}

export async function deleteSupplier(
  businessId,
  supplierId,
) {
  await api.delete(
    `/businesses/${businessId}/suppliers/${supplierId}/`,
  )
}
