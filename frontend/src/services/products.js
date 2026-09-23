import api from './api'

function normalizeListResponse(data) {
  if (Array.isArray(data)) {
    return data
  }

  if (Array.isArray(data?.results)) {
    return data.results
  }

  return []
}

export async function getProducts(businessId) {
  const response = await api.get(
    `/businesses/${businessId}/products/`
  )

  return normalizeListResponse(response.data)
}

export async function getCategories(businessId) {
  const response = await api.get(
    `/businesses/${businessId}/categories/`
  )

  return normalizeListResponse(response.data)
}

export async function createProduct(
  businessId,
  payload
) {
  const response = await api.post(
    `/businesses/${businessId}/products/`,
    payload
  )

  return response.data
}

export async function updateProduct(
  businessId,
  productId,
  payload
) {
  const response = await api.patch(
    `/businesses/${businessId}/products/${productId}/`,
    payload
  )

  return response.data
}
