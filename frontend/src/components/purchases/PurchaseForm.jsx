import PurchaseFormFields from './form/PurchaseFormFields'
import PurchaseItems from './form/PurchaseItems'

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
          <PurchaseFormFields
            suppliers={suppliers}
            form={form}
            onChange={onChange}
          />

          <PurchaseItems
            products={products}
            items={form.items}
            onItemChange={onItemChange}
            onAddItem={onAddItem}
            onRemoveItem={onRemoveItem}
          />

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
