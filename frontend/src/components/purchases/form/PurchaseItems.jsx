function PurchaseItems({
  products,
  items,
  onItemChange,
  onAddItem,
  onRemoveItem,
}) {
  return (
    <>
      <div className="purchase-items-header">
        <div>
          <span>LINE ITEMS</span>
          <h3>Products received</h3>
        </div>

        <button
          type="button"
          onClick={onAddItem}
        >
          + Add Product
        </button>
      </div>

      <div className="purchase-items">
        {items.map((item, index) => (
          <div
            className="purchase-item"
            key={index}
          >
            <label>
              Product
              <select
                value={item.product}
                onChange={(event) =>
                  onItemChange(
                    index,
                    'product',
                    event.target.value,
                  )
                }
                required
              >
                <option value="">
                  Select product
                </option>

                {products.map((product) => (
                  <option
                    key={product.id}
                    value={product.id}
                  >
                    {product.name}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Quantity
              <input
                type="number"
                min="0.01"
                step="0.01"
                value={item.quantity}
                onChange={(event) =>
                  onItemChange(
                    index,
                    'quantity',
                    event.target.value,
                  )
                }
                required
              />
            </label>

            <label>
              Unit cost
              <input
                type="number"
                min="0"
                step="0.01"
                value={item.unit_cost}
                onChange={(event) =>
                  onItemChange(
                    index,
                    'unit_cost',
                    event.target.value,
                  )
                }
                required
              />
            </label>

            <button
              type="button"
              className="danger"
              onClick={() =>
                onRemoveItem(index)
              }
              disabled={items.length === 1}
            >
              Remove
            </button>
          </div>
        ))}
      </div>
    </>
  )
}

export default PurchaseItems
