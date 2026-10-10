import api from './api'

export async function getPlans() {
  const response = await api.get('billing/plans/')

  return response.data
}

export async function getCurrentSubscription(
  businessId,
) {
  const response = await api.get(
    `businesses/${businessId}/subscription/`,
  )

  return response.data
}

export async function createPayment(
  businessId,
  paymentData,
) {
  const response = await api.post(
    `businesses/${businessId}/payments/`,
    paymentData,
  )

  return response.data
}
