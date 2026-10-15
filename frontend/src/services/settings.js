import api from './api'

export async function getProfile() {
  const response = await api.get('/auth/me/')
  return response.data
}

export async function updateProfile(payload) {
  const response = await api.patch(
    '/auth/me/',
    payload,
  )

  return response.data
}

export async function getBusiness(businessId) {
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

export async function addBusinessMember(
  businessId,
  payload,
) {
  const response = await api.post(
    `/businesses/${businessId}/members/`,
    payload,
  )

  return response.data
}

export async function updateBusinessMember(
  businessId,
  userId,
  payload,
) {
  const response = await api.patch(
    `/businesses/${businessId}/members/${userId}/`,
    payload,
  )

  return response.data
}

export async function deactivateBusinessMember(
  businessId,
  userId,
) {
  await api.delete(
    `/businesses/${businessId}/members/${userId}/`,
  )
}

export async function getBusinessInvitations(
  businessId,
) {
  const response = await api.get(
    `/businesses/${businessId}/invitations/`,
  )

  if (Array.isArray(response.data)) {
    return response.data
  }

  return response.data?.results || []
}

export async function createBusinessInvitation(
  businessId,
  payload,
) {
  const response = await api.post(
    `/businesses/${businessId}/invitations/`,
    payload,
  )

  return response.data
}

export async function revokeBusinessInvitation(
  businessId,
  invitationId,
) {
  await api.delete(
    `/businesses/${businessId}/invitations/${invitationId}/`,
  )
}

export async function acceptBusinessInvitation(token) {
  const response = await api.post(
    '/businesses/invitations/accept/',
    { token },
  )

  return response.data
}
