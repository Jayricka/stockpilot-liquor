import api from './api'

export async function startDemo() {
  const response = await api.post(
    '/demo/start/',
  )

  return response.data
}

export async function getDemoState(token) {
  const response = await api.get(
    `/demo/${token}/`,
  )

  return response.data
}

export async function receiveDemoStock(
  token,
  productId,
  quantity,
) {
  const response = await api.post(
    `/demo/${token}/purchase/`,
    {
      product_id: productId,
      quantity,
    },
  )

  return response.data
}

export async function makeDemoSale(
  token,
  productId,
  quantity,
) {
  const response = await api.post(
    `/demo/${token}/sale/`,
    {
      product_id: productId,
      quantity,
    },
  )

  return response.data
}
