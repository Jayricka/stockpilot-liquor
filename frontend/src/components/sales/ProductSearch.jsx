import {
  Search,
  X,
} from 'lucide-react'

function ProductSearch({
  value,
  onChange,
}) {
  return (
    <div className="product-search">
      <Search size={18} />

      <input
        type="search"
        value={value}
        onChange={(event) =>
          onChange(event.target.value)
        }
        placeholder="Search products or SKU..."
        aria-label="Search products"
      />

      {value && (
        <button
          type="button"
          onClick={() => onChange('')}
          aria-label="Clear search"
        >
          <X size={17} />
        </button>
      )}
    </div>
  )
}

export default ProductSearch
