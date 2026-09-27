import { useState } from 'react'

function useSaleCart() {
  const [cart, setCart] = useState([])

  function addToCart(product) {
    const stock = Number(
      product.stock_quantity || 0,
    )

    if (stock <= 0) {
      return
    }

    setCart((currentCart) => {
      const existing = currentCart.find(
        (item) =>
          item.id === product.id,
      )

      if (existing) {
        if (
          Number(existing.quantity) >=
          stock
        ) {
          return currentCart
        }

        return currentCart.map(
          (item) =>
            item.id === product.id
              ? {
                  ...item,
                  quantity:
                    Number(
                      item.quantity,
                    ) + 1,
                }
              : item,
        )
      }

      return [
        ...currentCart,
        {
          ...product,
          quantity: 1,
        },
      ]
    })
  }

  function updateQuantity(
    productId,
    quantity,
  ) {
    const product = cart.find(
      (item) =>
        item.id === productId,
    )

    if (!product) {
      return
    }

    const stock = Number(
      product.stock_quantity || 0,
    )

    const nextQuantity =
      Number(quantity)

    if (nextQuantity <= 0) {
      removeFromCart(productId)
      return
    }

    if (nextQuantity > stock) {
      return
    }

    setCart((currentCart) =>
      currentCart.map((item) =>
        item.id === productId
          ? {
              ...item,
              quantity:
                nextQuantity,
            }
          : item,
      ),
    )
  }

  function removeFromCart(productId) {
    setCart((currentCart) =>
      currentCart.filter(
        (item) =>
          item.id !== productId,
      ),
    )
  }

  function clearCart() {
    setCart([])
  }

  return {
    cart,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
  }
}

export default useSaleCart
