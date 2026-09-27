import { useState } from 'react'

import useSaleCart from './hooks/useSaleCart'
import useSaleCheckout from './hooks/useSaleCheckout'
import useSaleActions from './hooks/useSaleActions'
import ProductSearch from './ProductSearch'
import ProductGrid from './ProductGrid'
import Cart from './Cart'
import SaleSummary from './SaleSummary'

function POS({
  products,
  businessId,
  businessName,
  loading,
  onSaleCompleted,
}) {
  const {
    cart,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
  } = useSaleCart()

  const [search, setSearch] =
    useState('')

  const {
    discount,
    setDiscount,
    paymentMethod,
    setPaymentMethod,
    amountReceived,
    setAmountReceived,
    subtotal,
    discountAmount,
    total,
    change,
  } = useSaleCheckout(cart)

  function handleAddToCart(product) {
    setError('')
    addToCart(product)
  }

  const {
    saving,
    error,
    setError,
    handleCompleteSale,
  } = useSaleActions({
    businessId,
    cart,
    discountAmount,
    subtotal,
    paymentMethod,
    amountReceived,
    total,
    clearCart,
    setDiscount,
    setAmountReceived,
    setPaymentMethod,
    onSaleCompleted,
  })


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
            onAdd={handleAddToCart}
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
