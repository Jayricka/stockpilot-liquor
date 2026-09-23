import api from './api'

export async function getProfile() {
  const response = await api.get(
    '/auth/me/',
  )

  return response.data
}

export async function updateProfile(
  payload,
) {
  const response = await api.patch(
    '/auth/me/',
    payload,
  )

  return response.data
}

export async function getBusiness(
  businessId,
) {
  const response = await api.get(
    `/businesses/${businessId}/`,
  )

  return response.data
}

export async function updateBusiness(
  businessId,
  payload,
) {
  const response = await api.patch(
    `/businesses/${businessId}/`,
    payload,
  )

  return response.data
}

export async function getBusinessMembers(
  businessId,
) {
  const response = await api.get(
    `/businesses/${businessId}/members/`,
  )

  if (Array.isArray(response.data)) {
    return response.data
  }

  return response.data?.results || []
}
