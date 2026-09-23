import {
  useMemo,
  useState,
} from 'react'

import ProductSearch from './ProductSearch'
import ProductGrid from './ProductGrid'
import Cart from './Cart'
import SaleSummary from './SaleSummary'

import {
  completeSale,
  createSale,
} from '../../services/sales'

function getErrorMessage(error) {
  const data = error?.response?.data

  if (!data) {
    return 'Unable to complete the sale.'
  }

  if (typeof data.detail === 'string') {
    return data.detail
  }

  if (Array.isArray(data.detail)) {
    return data.detail.join(', ')
  }

  if (Array.isArray(data.non_field_errors)) {
    return data.non_field_errors.join(', ')
  }

  const firstError = Object.values(data)[0]

  if (Array.isArray(firstError)) {
    return firstError.join(', ')
  }

  if (typeof firstError === 'string') {
    return firstError
  }

  return 'Unable to complete the sale.'
}

function getToday() {
  const now = new Date()

  const year = now.getFullYear()
  const month = String(
    now.getMonth() + 1,
  ).padStart(2, '0')

  const day = String(
    now.getDate(),
  ).padStart(2, '0')

  return `${year}-${month}-${day}`
}

function POS({
  products,
  businessId,
  businessName,
  loading,
  onSaleCompleted,
}) {
  const [cart, setCart] = useState([])

  const [search, setSearch] =
    useState('')

  const [discount, setDiscount] =
    useState('')

  const [paymentMethod, setPaymentMethod] =
    useState('CASH')

  const [amountReceived, setAmountReceived] =
    useState('')

  const [saving, setSaving] =
    useState(false)

  const [error, setError] =
    useState('')

  const subtotal = useMemo(
    () =>
      cart.reduce(
        (total, item) =>
          total +
          Number(item.selling_price || 0) *
            Number(item.quantity || 0),
        0,
      ),
    [cart],
  )

  const discountAmount =
    Number(discount || 0)

  const total = Math.max(
    subtotal - discountAmount,
    0,
  )

  const change =
    paymentMethod === 'CASH'
      ? Math.max(
          Number(amountReceived || 0) -
            total,
          0,
        )
      : 0

  function addToCart(product) {
    setError('')

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

  async function handleCompleteSale() {
    setError('')

    if (!businessId) {
      setError(
        'Please select a business first.',
      )
      return
    }

    if (!cart.length) {
      setError(
        'Add at least one product to the cart.',
      )
      return
    }

    if (discountAmount < 0) {
      setError(
        'Discount cannot be negative.',
      )
      return
    }

    if (discountAmount > subtotal) {
      setError(
        'Discount cannot exceed the sale subtotal.',
      )
      return
    }

    if (
      paymentMethod === 'CASH' &&
      Number(amountReceived || 0) <
        total
    ) {
      setError(
        'Amount received is insufficient.',
      )
      return
    }

    try {
      setSaving(true)

      const payload = {
        invoice_number: `SP-${Date.now()}`,
        discount_amount:
          discountAmount,
        payment_method:
          paymentMethod,
        sale_date: getToday(),
        items: cart.map((item) => ({
          product: item.id,
          quantity: item.quantity,
        })),
      }

      const sale = await createSale(
        businessId,
        payload,
      )

      await completeSale(
        businessId,
        sale.id,
      )

      setCart([])
      setDiscount('')
      setAmountReceived('')
      setPaymentMethod('CASH')

      if (onSaleCompleted) {
        onSaleCompleted()
      }
    } catch (requestError) {
      setError(
        getErrorMessage(requestError),
      )
    } finally {
      setSaving(false)
    }
  }

  return (
    <section className="pos-workspace">
      <div className="pos-heading">
        <div>
          <span>Current business</span>

          <h2>{businessName}</h2>
        </div>

        <span className="pos-product-count">
          {products.length} products
        </span>
      </div>

      {error && (
        <div
          className="pos-error"
          role="alert"
        >
          {error}
        </div>
      )}

      <div className="pos-layout">
        <section className="pos-products">
          <ProductSearch
            value={search}
            onChange={setSearch}
          />

          <ProductGrid
            products={products}
            search={search}
            loading={loading}
            onAdd={addToCart}
          />
        </section>

        <aside className="pos-sidebar">
          <Cart
            items={cart}
            onQuantityChange={
              updateQuantity
            }
            onRemove={removeFromCart}
          />

          <SaleSummary
            subtotal={subtotal}
            discount={discount}
            onDiscountChange={
              setDiscount
            }
            total={total}
            paymentMethod={
              paymentMethod
            }
            onPaymentMethodChange={
              setPaymentMethod
            }
            amountReceived={
              amountReceived
            }
            onAmountReceivedChange={
              setAmountReceived
            }
            change={change}
            onComplete={
              handleCompleteSale
            }
            loading={saving}
          />
        </aside>
      </div>
    </section>
  )
}

export default POS
