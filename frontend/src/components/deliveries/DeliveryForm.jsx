function DeliveryForm({
  sales,
  form,
  saving,
  onChange,
  onSubmit,
  onClose,
}) {
  return (
    <div
      className="delivery-modal"
      role="dialog"
      aria-modal="true"
      aria-labelledby="delivery-modal-title"
    >
      <div className="delivery-modal-card">
        <header>
          <div>
            <span className="delivery-modal-eyebrow">
              FULFILLMENT
            </span>

            <h2 id="delivery-modal-title">
              New Delivery
            </h2>
          </div>

          <button
            type="button"
            onClick={onClose}
            disabled={saving}
            aria-label="Close delivery form"
          >
            ×
          </button>
        </header>

        <form onSubmit={onSubmit}>
          <label>
            Completed sale
            <select
              name="sale"
              value={form.sale}
              onChange={onChange}
              required
            >
              <option value="">
                Select a completed sale
              </option>

              {sales.map((sale) => (
                <option
                  key={sale.id}
                  value={sale.id}
                >
                  {sale.invoice_number} — KES{' '}
                  {Number(
                    sale.total_amount || 0,
                  ).toLocaleString()}
                </option>
              ))}
            </select>
          </label>

          <div className="delivery-form-grid">
            <label>
              Customer name
              <input
                name="customer_name"
                value={form.customer_name}
                onChange={onChange}
                placeholder="e.g. John Kamau"
                required
              />
            </label>

            <label>
              Phone
              <input
                name="customer_phone"
                value={form.customer_phone}
                onChange={onChange}
                placeholder="0700000000"
                required
              />
            </label>
          </div>

          <label>
            Delivery address
            <textarea
              name="delivery_address"
              value={form.delivery_address}
              onChange={onChange}
              rows="3"
              placeholder="Enter the customer's delivery address"
              required
            />
          </label>

          <label>
            Delivery fee
            <input
              type="number"
              name="delivery_fee"
              value={form.delivery_fee}
              onChange={onChange}
              min="0"
              step="0.01"
              placeholder="0"
            />
          </label>

          <label>
            Notes
            <textarea
              name="notes"
              value={form.notes}
              onChange={onChange}
              rows="3"
              placeholder="Optional delivery instructions"
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
              disabled={saving || !sales.length}
            >
              {saving
                ? 'Creating...'
                : 'Create Delivery'}
            </button>
          </footer>
        </form>
      </div>
    </div>
  )
}

export default DeliveryForm
