import api from './api'

export async function getReport(businessId) {
  const response = await api.get(
    `businesses/${businessId}/reports/dashboard/`,
  )

  return response.data
}
