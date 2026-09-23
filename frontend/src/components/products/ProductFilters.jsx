import {
  Search,
  SlidersHorizontal,
  X,
} from 'lucide-react'

const STOCK_OPTIONS = [
  {
    value: 'in-stock',
    label: 'In stock',
  },
  {
    value: 'low-stock',
    label: 'Low stock',
  },
  {
    value: 'out-of-stock',
    label: 'Out of stock',
  },
]

const STATUS_OPTIONS = [
  {
    value: 'active',
    label: 'Active',
  },
  {
    value: 'inactive',
    label: 'Inactive',
  },
]

function SelectFilter({
  value,
  onChange,
  options,
  placeholder,
}) {
  return (
    <select
      value={value}
      onChange={(event) =>
        onChange(event.target.value)
      }
      className="h-10 min-w-[145px] rounded-lg border border-slate-200 bg-white px-3 text-sm font-medium text-slate-700 outline-none transition hover:border-slate-300 focus:border-slate-400 focus:ring-2 focus:ring-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:border-slate-600 dark:focus:border-slate-500 dark:focus:ring-slate-700"
    >
      <option value="">
        {placeholder}
      </option>

      {options.map((option) => (
        <option
          key={option.value}
          value={option.value}
        >
          {option.label}
        </option>
      ))}
    </select>
  )
}

function ProductFilters({
  search,
  catalogFilter,
  catalogGroups,
  catalogCounts,
  categoryFilter,
  stockFilter,
  statusFilter,
  categories = [],
  onSearchChange,
  onCatalogChange,
  onCategoryChange,
  onStockChange,
  onStatusChange,
  resultCount,
  totalCount,
  onClear,
}) {
  const hasFilters =
    Boolean(search.trim()) ||
    catalogFilter !== 'all' ||
    categoryFilter !== 'all' ||
    stockFilter !== 'all' ||
    statusFilter !== 'all'

  const categoryOptions = categories.map(
    (category) => ({
      value: String(category.id),
      label: category.name,
    }),
  )

  return (
    <section className="mb-5">
      {/* CATALOG */}
      <div className="border-b border-slate-200 dark:border-slate-800">
        <div className="flex items-center gap-3">
          <div className="hidden shrink-0 py-3 text-[11px] font-bold uppercase tracking-[0.14em] text-slate-400 sm:block">
            Catalog
          </div>

          <div
            className="scrollbar-none flex min-w-0 flex-1 items-center gap-1 overflow-x-auto"
            role="tablist"
            aria-label="Product catalog"
          >
            {catalogGroups.map((item) => {
              const isActive =
                catalogFilter === item.value

              const count =
                catalogCounts[item.countKey] || 0

              return (
                <button
                  key={item.value}
                  type="button"
                  role="tab"
                  aria-selected={isActive}
                  onClick={() =>
                    onCatalogChange(
                      item.value,
                    )
                  }
                  className={`group relative flex h-12 shrink-0 items-center gap-2 whitespace-nowrap border-b-2 px-3 text-sm font-medium transition ${
                    isActive
                      ? 'border-slate-950 text-slate-950 dark:border-slate-200 dark:text-slate-100'
                      : 'border-transparent text-slate-500 hover:border-slate-300 hover:text-slate-800 dark:text-slate-400 dark:hover:border-slate-600 dark:hover:text-slate-200'
                  }`}
                >
                  <span>{item.label}</span>

                  <span
                    className={`rounded-full px-2 py-0.5 text-[11px] font-semibold tabular-nums ${
                      isActive
                        ? 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'
                        : 'bg-slate-50 text-slate-400 group-hover:bg-slate-100 group-hover:text-slate-600 dark:bg-slate-900 dark:text-slate-500 dark:group-hover:bg-slate-800 dark:group-hover:text-slate-300'
                    }`}
                  >
                    {count}
                  </span>
                </button>
              )
            })}
          </div>
        </div>
      </div>

      {/* FILTER BAR */}
      <div className="mt-4 rounded-xl border border-slate-200 bg-white p-3 shadow-sm dark:border-slate-700 dark:bg-slate-900">
        <div className="flex flex-col gap-3 xl:flex-row xl:items-center">
          {/* Search */}
          <div className="relative min-w-0 flex-1">
            <Search
              size={17}
              className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-slate-400"
            />

            <input
              type="search"
              value={search}
              onChange={(event) =>
                onSearchChange(
                  event.target.value,
                )
              }
              placeholder="Search products, brands or SKU..."
              className="h-10 w-full rounded-lg border border-slate-200 bg-slate-50/50 pl-9 pr-9 text-sm text-slate-800 outline-none transition placeholder:text-slate-400 hover:border-slate-300 focus:border-slate-400 focus:bg-white focus:ring-2 focus:ring-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:placeholder:text-slate-500 dark:hover:border-slate-600 dark:focus:border-slate-500 dark:focus:bg-slate-800 dark:focus:ring-slate-700"
            />

            {search && (
              <button
                type="button"
                onClick={() =>
                  onSearchChange('')
                }
                aria-label="Clear search"
                className="absolute right-3 top-1/2 -translate-y-1/2 rounded-md p-0.5 text-slate-400 transition hover:bg-slate-100 hover:text-slate-700 dark:hover:bg-slate-700 dark:hover:text-slate-200"
              >
                <X size={15} />
              </button>
            )}
          </div>

          {/* Secondary filters */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="flex items-center gap-1.5 text-slate-400">
              <SlidersHorizontal size={14} />
              <span className="hidden text-xs font-medium sm:inline">
                Filter
              </span>
            </div>

            <SelectFilter
              value={
                categoryFilter === 'all'
                  ? ''
                  : categoryFilter
              }
              onChange={(value) =>
                onCategoryChange(
                  value || 'all',
                )
              }
              options={categoryOptions}
              placeholder="Category"
            />

            <SelectFilter
              value={
                stockFilter === 'all'
                  ? ''
                  : stockFilter
              }
              onChange={(value) =>
                onStockChange(
                  value || 'all',
                )
              }
              options={STOCK_OPTIONS}
              placeholder="Stock"
            />

            <SelectFilter
              value={
                statusFilter === 'all'
                  ? ''
                  : statusFilter
              }
              onChange={(value) =>
                onStatusChange(
                  value || 'all',
                )
              }
              options={STATUS_OPTIONS}
              placeholder="Status"
            />

            {hasFilters && (
              <button
                type="button"
                onClick={onClear}
                className="inline-flex h-10 shrink-0 items-center justify-center gap-1.5 rounded-lg px-3 text-sm font-medium text-slate-500 transition hover:bg-slate-100 hover:text-slate-900 dark:text-slate-400 dark:hover:bg-slate-800 dark:hover:text-slate-200"
              >
                <X size={15} />
                Clear
              </button>
            )}
          </div>
        </div>

        {/* Result summary */}
        <div className="mt-3 flex items-center justify-between border-t border-slate-100 pt-3 dark:border-slate-800">
          <p className="text-xs text-slate-500">
            {hasFilters ? (
              <>
                Showing{' '}
                <span className="font-semibold text-slate-700 dark:text-slate-300">
                  {resultCount}
                </span>{' '}
                of{' '}
                <span className="font-semibold text-slate-700 dark:text-slate-300">
                  {totalCount}
                </span>{' '}
                products
              </>
            ) : (
              <>
                <span className="font-semibold text-slate-700 dark:text-slate-300">
                  {totalCount}
                </span>{' '}
                {totalCount === 1
                  ? 'product'
                  : 'products'}
              </>
            )}
          </p>

          {hasFilters && (
            <span className="hidden text-xs text-slate-400 sm:block">
              Filters applied
            </span>
          )}
        </div>
      </div>
    </section>
  )
}

export default ProductFilters
