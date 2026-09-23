function PurchaseForm({
  suppliers,
  products,
  form,
  saving,
  onChange,
  onItemChange,
  onAddItem,
  onRemoveItem,
  onSubmit,
  onClose,
}) {
  return (
    <div
      className="purchase-modal"
      role="dialog"
      aria-modal="true"
      aria-labelledby="purchase-modal-title"
    >
      <div className="purchase-modal-card">
        <header>
          <div>
            <span className="purchase-modal-eyebrow">
              PROCUREMENT
            </span>

            <h2 id="purchase-modal-title">
              New Purchase
            </h2>
          </div>

          <button
            type="button"
            onClick={onClose}
            disabled={saving}
            aria-label="Close purchase form"
          >
            ×
          </button>
        </header>

        <form onSubmit={onSubmit}>
          <div className="purchase-form-grid">
            <label>
              Supplier
              <select
                name="supplier"
                value={form.supplier}
                onChange={onChange}
                required
              >
                <option value="">
                  Select supplier
                </option>

                {suppliers.map((supplier) => (
                  <option
                    key={supplier.id}
                    value={supplier.id}
                  >
                    {supplier.name}
                  </option>
                ))}
              </select>
            </label>

            <label>
              Reference number
              <input
                name="reference_number"
                value={form.reference_number}
                onChange={onChange}
                placeholder="e.g. PO-00021"
                required
              />
            </label>

            <label>
              Purchase date
              <input
                type="date"
                name="purchase_date"
                value={form.purchase_date}
                onChange={onChange}
                required
              />
            </label>
          </div>

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
            {form.items.map((item, index) => (
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
                  disabled={form.items.length === 1}
                >
                  Remove
                </button>
              </div>
            ))}
          </div>

          <label>
            Notes
            <textarea
              name="notes"
              value={form.notes}
              onChange={onChange}
              rows="3"
              placeholder="Optional purchase notes"
            />
          </label>

          <footer>
            <button
              type="button"
              onClick={onClose}
              disabled={saving}
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={
                saving ||
                !suppliers.length ||
                !products.length
              }
            >
              {saving
                ? 'Creating...'
                : 'Create Purchase'}
            </button>
          </footer>
        </form>
      </div>
    </div>
  )
}

export default PurchaseForm
