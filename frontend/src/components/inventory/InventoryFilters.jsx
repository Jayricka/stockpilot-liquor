import { Search, SlidersHorizontal } from 'lucide-react'

function InventoryFilters({
  search,
  onSearchChange,
  lowStockOnly,
  onLowStockChange,
}) {
  return (
    <div className="inventory-filters">
      <label className="inventory-search">
        <Search size={17} />

        <input
          type="search"
          placeholder="Search products or SKU..."
          value={search}
          onChange={(event) =>
            onSearchChange(event.target.value)
          }
        />
      </label>

      <label className="low-stock-filter">
        <SlidersHorizontal size={16} />

        <input
          type="checkbox"
          checked={lowStockOnly}
          onChange={(event) =>
            onLowStockChange(event.target.checked)
          }
        />

        Low stock only
      </label>
    </div>
  )
}

export default InventoryFilters
