import api from './api'

export async function getBusinesses() {
  const response = await api.get('businesses/')
  return response.data
}

export async function getDashboard(businessId) {
  const response = await api.get(
    `businesses/${businessId}/reports/dashboard/`,
  )

  return response.data
}
