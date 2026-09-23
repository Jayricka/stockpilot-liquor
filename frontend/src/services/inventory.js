import api from './api'

export async function getProducts(businessId) {
  const response = await api.get(
    `businesses/${businessId}/products/`,
  )

  return response.data
}
