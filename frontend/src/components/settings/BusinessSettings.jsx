function BusinessSettings({
  business,
  form,
  saving,
  editable,
  onChange,
  onSubmit,
}) {
  return (
    <article className="settings-panel">
      <header>
        <div>
          <span>BUSINESS</span>

          <h2>Business information</h2>

          <p>
            Keep your business details up to date.
          </p>
        </div>

        <span className="settings-role">
          {business.role || 'Member'}
        </span>
      </header>

      <form onSubmit={onSubmit}>
        <div className="settings-form-grid">
          <label>
            Business name

            <input
              name="name"
              value={form.name}
              onChange={onChange}
              required
              disabled={!editable}
            />
          </label>

          <label>
            Business type

            <input
              name="business_type"
              value={form.business_type}
              onChange={onChange}
              required
              disabled={!editable}
            />
          </label>

          <label>
            Phone

            <input
              name="phone"
              value={form.phone}
              onChange={onChange}
              required
              disabled={!editable}
            />
          </label>

          <label>
            Email

            <input
              type="email"
              name="email"
              value={form.email}
              onChange={onChange}
              disabled={!editable}
            />
          </label>
        </div>

        <label>
          Address

          <textarea
            name="address"
            value={form.address}
            onChange={onChange}
            rows="3"
            disabled={!editable}
          />
        </label>

        <label>
          License number

          <input
            name="license_number"
            value={form.license_number}
            onChange={onChange}
            placeholder="Optional"
            disabled={!editable}
          />
        </label>

        {editable && (
          <button
            type="submit"
            disabled={saving}
          >
            {saving
              ? 'Saving...'
              : 'Save Business'}
          </button>
        )}
      </form>
    </article>
  )
}

export default BusinessSettings
