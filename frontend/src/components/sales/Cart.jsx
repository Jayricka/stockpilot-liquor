import {
  Minus,
  Plus,
  Trash2,
} from 'lucide-react'

function Cart({
  items,
  onQuantityChange,
  onRemove,
}) {
  return (
    <section className="sale-cart">
      <div className="sale-section-header">
        <div>
          <span>Current sale</span>
          <h2>Cart</h2>
        </div>

        <span>
          {items.length} items
        </span>
      </div>

      {!items.length ? (
        <div className="sale-cart-empty">
          <h3>Your cart is empty</h3>

          <p>
            Select products to start a sale.
          </p>
        </div>
      ) : (
        <div className="sale-cart-items">
          {items.map((item) => {
            const quantity =
              Number(item.quantity || 0)

            const price =
              Number(
                item.selling_price || 0,
              )

            const lineTotal =
              quantity * price

            const stock =
              Number(
                item.stock_quantity || 0,
              )

            return (
              <article
                key={item.id}
                className="sale-cart-item"
              >
                <div className="sale-cart-item-info">
                  <strong>
                    {item.name}
                  </strong>

                  <span>
                    KES{' '}
                    {price.toLocaleString()}{' '}
                    /{' '}
                    {item.unit ||
                      'unit'}
                  </span>
                </div>

                <div className="sale-cart-item-actions">
                  <div className="quantity-control">
                    <button
                      type="button"
                      onClick={() =>
                        onQuantityChange(
                          item.id,
                          quantity - 1,
                        )
                      }
                      aria-label="Decrease quantity"
                    >
                      <Minus size={14} />
                    </button>

                    <span>
                      {quantity}
                    </span>

                    <button
                      type="button"
                      disabled={
                        quantity >=
                        stock
                      }
                      onClick={() =>
                        onQuantityChange(
                          item.id,
                          quantity + 1,
                        )
                      }
                      aria-label="Increase quantity"
                    >
                      <Plus size={14} />
                    </button>
                  </div>

                  <strong>
                    KES{' '}
                    {lineTotal.toLocaleString()}
                  </strong>

                  <button
                    type="button"
                    className="remove-cart-item"
                    onClick={() =>
                      onRemove(item.id)
                    }
                    aria-label={`Remove ${item.name}`}
                  >
                    <Trash2 size={16} />
                  </button>
                </div>
              </article>
            )
          })}
        </div>
      )}
    </section>
  )
}

export default Cart
