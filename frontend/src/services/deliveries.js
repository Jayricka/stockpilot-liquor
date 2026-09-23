import api from './api'

function normalizeList(data) {
  if (Array.isArray(data)) {
    return data
  }

  return data?.results || []
}

export async function getDeliveries(
  businessId,
  status = '',
) {
  const params = status
    ? { status }
    : undefined

  const response = await api.get(
    `/businesses/${businessId}/deliveries/`,
    { params },
  )

  return normalizeList(response.data)
}

export async function getDelivery(
  businessId,
  deliveryId,
) {
  const response = await api.get(
    `/businesses/${businessId}/deliveries/${deliveryId}/`,
  )

  return response.data
}

export async function getBusinessMembers(
  businessId,
) {
  const response = await api.get(
    `/businesses/${businessId}/members/`,
  )

  return normalizeList(response.data)
}

export async function createDelivery(
  businessId,
  payload,
) {
  const response = await api.post(
    `/businesses/${businessId}/deliveries/`,
    payload,
  )

  return response.data
}

export async function assignDelivery(
  businessId,
  deliveryId,
  userId,
) {
  const response = await api.post(
    `/businesses/${businessId}/deliveries/${deliveryId}/assign/`,
    {
      assigned_to: userId,
    },
  )

  return response.data
}

export async function startDelivery(
  businessId,
  deliveryId,
) {
  const response = await api.post(
    `/businesses/${businessId}/deliveries/${deliveryId}/start/`,
  )

  return response.data
}

export async function completeDelivery(
  businessId,
  deliveryId,
) {
  const response = await api.post(
    `/businesses/${businessId}/deliveries/${deliveryId}/complete/`,
  )

  return response.data
}

export async function cancelDelivery(
  businessId,
  deliveryId,
) {
  const response = await api.post(
    `/businesses/${businessId}/deliveries/${deliveryId}/cancel/`,
  )

  return response.data
}
