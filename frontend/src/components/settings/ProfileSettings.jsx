function ProfileSettings({
  profile,
  form,
  saving,
  onChange,
  onSubmit,
}) {
  return (
    <article className="settings-panel">
      <header>
        <div>
          <span>ACCOUNT</span>

          <h2>Profile</h2>

          <p>
            Update your personal information.
          </p>
        </div>
      </header>

      <form onSubmit={onSubmit}>
        <div className="settings-form-grid">
          <label>
            First name

            <input
              name="first_name"
              value={form.first_name}
              onChange={onChange}
              placeholder="First name"
              required
            />
          </label>

          <label>
            Last name

            <input
              name="last_name"
              value={form.last_name}
              onChange={onChange}
              placeholder="Last name"
              required
            />
          </label>
        </div>

        <label>
          Email

          <input
            type="email"
            value={profile.email || ''}
            disabled
          />
        </label>

        <button
          type="submit"
          disabled={saving}
        >
          {saving
            ? 'Saving...'
            : 'Save Profile'}
        </button>
      </form>
    </article>
  )
}

export default ProfileSettings
