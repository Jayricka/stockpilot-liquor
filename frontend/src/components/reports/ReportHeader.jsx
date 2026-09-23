function ReportHeader({
  businesses,
  businessId,
  onBusinessChange,
  date,
}) {
  return (
    <header className="reports-header">
      <div>
        <span className="reports-eyebrow">
          BUSINESS INTELLIGENCE
        </span>

        <h1>Reports</h1>

        <p>
          Understand sales, inventory, products,
          and business activity.
        </p>
      </div>

      <div className="reports-header-actions">
        <select
          value={businessId || ''}
          onChange={(event) =>
            onBusinessChange(
              Number(event.target.value),
            )
          }
          aria-label="Select business"
        >
          {businesses.map((business) => (
            <option
              key={business.id}
              value={business.id}
            >
              {business.name}
            </option>
          ))}
        </select>

        {date && (
          <span className="reports-date">
            {new Date(`${date}T00:00:00`).toLocaleDateString(
              'en-KE',
              {
                day: 'numeric',
                month: 'short',
                year: 'numeric',
              },
            )}
          </span>
        )}
      </div>
    </header>
  )
}

export default ReportHeader
