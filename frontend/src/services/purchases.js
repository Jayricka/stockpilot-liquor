import api from './api'

function normalizeList(data) {
  if (Array.isArray(data)) {
    return data
  }

  return data?.results || []
}

export async function getPurchases(
  businessId,
  status = '',
) {
  const params = status
    ? { status }
    : undefined

  const response = await api.get(
    `/businesses/${businessId}/purchases/`,
    { params },
  )

  return normalizeList(response.data)
}

export async function getPurchase(
  businessId,
  purchaseId,
) {
  const response = await api.get(
    `/businesses/${businessId}/purchases/${purchaseId}/`,
  )

  return response.data
}

export async function createPurchase(
  businessId,
  payload,
) {
  const response = await api.post(
    `/businesses/${businessId}/purchases/`,
    payload,
  )

  return response.data
}

export async function completePurchase(
  businessId,
  purchaseId,
) {
  const response = await api.post(
    `/businesses/${businessId}/purchases/${purchaseId}/complete/`,
  )

  return response.data
}

export async function cancelPurchase(
  businessId,
  purchaseId,
) {
  const response = await api.post(
    `/businesses/${businessId}/purchases/${purchaseId}/cancel/`,
  )

  return response.data
}
