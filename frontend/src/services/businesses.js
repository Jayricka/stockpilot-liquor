import api from './api'

export async function onboardBusiness(businessData) {
  const response = await api.post(
    'businesses/onboard/',
    businessData,
  )

  return response.data
}
