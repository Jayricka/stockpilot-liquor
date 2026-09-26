import api from './api'

export async function getPlans() {
  const response = await api.get('billing/plans/')

  return response.data
}

export async function getCurrentSubscription() {
  const response = await api.get(
    'billing/subscription/',
  )

  return response.data
}
