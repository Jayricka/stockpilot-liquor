import api from './api'

function normalizeListResponse(data) {
  if (Array.isArray(data)) {
    return data
  }

  return data?.results || []
}

export async function getSales(businessId, params = {}) {
  const response = await api.get(
    `/businesses/${businessId}/sales/`,
    { params },
  )

  return normalizeListResponse(response.data)
}

export async function getSale(
  businessId,
  saleId,
) {
  const response = await api.get(
    `/businesses/${businessId}/sales/${saleId}/`,
  )

  return response.data
}

export async function createSale(
  businessId,
  payload,
) {
  const response = await api.post(
    `/businesses/${businessId}/sales/`,
    payload,
  )

  return response.data
}

export async function completeSale(
  businessId,
  saleId,
) {
  const response = await api.post(
    `/businesses/${businessId}/sales/${saleId}/complete/`,
  )

  return response.data
}

export async function cancelSale(
  businessId,
  saleId,
) {
  const response = await api.post(
    `/businesses/${businessId}/sales/${saleId}/cancel/`,
  )

  return response.data
}
