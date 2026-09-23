import { Building2, ChevronDown } from 'lucide-react'

function DashboardHeader({
  businesses,
  businessId,
  onBusinessChange,
  date,
}) {
  return (
    <header className="dashboard-header">
      <div>
        <span className="dashboard-eyebrow">
          {date}
        </span>

        <h1>Business overview</h1>

        <p>
          Monitor sales, inventory and daily operations.
        </p>
      </div>

      <label className="business-selector">
        <Building2 size={17} />

        <select
          value={businessId || ''}
          onChange={(event) =>
            onBusinessChange(Number(event.target.value))
          }
        >
          {businesses.map((item) => (
            <option key={item.id} value={item.id}>
              {item.name}
            </option>
          ))}
        </select>

        <ChevronDown size={15} />
      </label>
    </header>
  )
}

export default DashboardHeader
