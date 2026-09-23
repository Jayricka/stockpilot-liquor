import { Package } from 'lucide-react'

function InventoryHeader({ businesses, businessId, onBusinessChange }) {
  return (
    <header className="inventory-header">
      <div>
        <span className="inventory-eyebrow">
          Stock management
        </span>

        <h1>Inventory</h1>

        <p>
          Monitor products, stock levels and reorder needs.
        </p>
      </div>

      <label className="inventory-business-selector">
        <Package size={17} />

        <select
          value={businessId || ''}
          onChange={(event) =>
            onBusinessChange(Number(event.target.value))
          }
        >
          {businesses.map((business) => (
            <option key={business.id} value={business.id}>
              {business.name}
            </option>
          ))}
        </select>
      </label>
    </header>
  )
}

export default InventoryHeader
