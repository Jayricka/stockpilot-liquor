function SupplierForm({
  form,
  editingSupplier,
  saving,
  onChange,
  onSubmit,
  onClose,
}) {
  return (
    <div
      className="supplier-modal"
      role="dialog"
      aria-modal="true"
      aria-labelledby="supplier-modal-title"
    >
      <div className="supplier-modal-card">
        <header>
          <h2 id="supplier-modal-title">
            {editingSupplier
              ? 'Edit Supplier'
              : 'Add Supplier'}
          </h2>

          <button
            type="button"
            onClick={onClose}
            disabled={saving}
            aria-label="Close supplier form"
          >
            ×
          </button>
        </header>

        <form onSubmit={onSubmit}>
          <label>
            Supplier name
            <input
              name="name"
              value={form.name}
              onChange={onChange}
              placeholder="e.g. Pattialla Distillers"
              required
              autoFocus
            />
          </label>

          <label>
            Phone
            <input
              name="phone"
              value={form.phone}
              onChange={onChange}
              placeholder="0700000000"
            />
          </label>

          <label>
            Email
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={onChange}
              placeholder="supplier@example.com"
            />
          </label>

          <label>
            Address
            <input
              name="address"
              value={form.address}
              onChange={onChange}
              placeholder="Supplier address"
            />
          </label>

          <label>
            Notes
            <textarea
              name="notes"
              value={form.notes}
              onChange={onChange}
              rows="3"
              placeholder="Optional supplier notes"
            />
          </label>

          <label className="supplier-active">
            <input
              type="checkbox"
              name="is_active"
              checked={form.is_active}
              onChange={onChange}
            />

            Active supplier
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
              disabled={saving}
            >
              {saving
                ? 'Saving...'
                : editingSupplier
                  ? 'Save Changes'
                  : 'Add Supplier'}
            </button>
          </footer>
        </form>
      </div>
    </div>
  )
}

export default SupplierForm
