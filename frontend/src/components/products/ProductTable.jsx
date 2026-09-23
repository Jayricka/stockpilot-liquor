import {
  Edit3,
  PackageOpen,
  SearchX,
} from 'lucide-react'

function formatCurrency(value) {
  const amount = Number(value || 0)

  return new Intl.NumberFormat('en-KE', {
    style: 'currency',
    currency: 'KES',
    maximumFractionDigits: 0,
  }).format(amount)
}

function formatQuantity(value) {
  const amount = Number(value || 0)

  return new Intl.NumberFormat('en-KE', {
    maximumFractionDigits: 2,
  }).format(amount)
}

function getStockState(product) {
  const quantity = Number(
    product.stock_quantity || 0,
  )

  const reorderLevel = Number(
    product.reorder_level || 0,
  )

  if (quantity <= 0) {
    return {
      label: 'Out of stock',
      dot: 'bg-red-500',
      text: 'text-red-700',
      background: 'bg-red-50',
    }
  }

  if (quantity <= reorderLevel) {
    return {
      label: 'Low stock',
      dot: 'bg-amber-500',
      text: 'text-amber-700',
      background: 'bg-amber-50',
    }
  }

  return {
    label: 'In stock',
    dot: 'bg-emerald-500',
    text: 'text-emerald-700',
    background: 'bg-emerald-50',
  }
}

function StockIndicator({ product }) {
  const state = getStockState(product)

  const unit = String(
    product.unit || 'piece',
  ).toLowerCase()

  return (
    <div className="min-w-[125px]">
      <div className="text-right text-sm font-semibold tabular-nums text-slate-900 dark:text-slate-100">
        {formatQuantity(
          product.stock_quantity,
        )}{' '}
        <span className="text-xs font-normal text-slate-400">
          {unit}
        </span>
      </div>

      <div className="mt-1 flex justify-end">
        <span
          className={`inline-flex items-center gap-1.5 rounded-full px-2 py-0.5 text-[11px] font-medium ${state.background} ${state.text}`}
        >
          <span
            className={`h-1.5 w-1.5 rounded-full ${state.dot}`}
          />

          {state.label}
        </span>
      </div>
    </div>
  )
}

function StatusBadge({ active }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium ${
        active
          ? 'bg-emerald-50 text-emerald-700'
          : 'bg-slate-100 text-slate-500'
      }`}
    >
      <span
        className={`h-1.5 w-1.5 rounded-full ${
          active
            ? 'bg-emerald-500'
            : 'bg-slate-400'
        }`}
      />

      {active ? 'Active' : 'Inactive'}
    </span>
  )
}

function LoadingRows() {
  return (
    <>
      {Array.from({ length: 6 }).map(
        (_, rowIndex) => (
          <tr key={rowIndex}>
            <td className="px-5 py-4">
              <div className="flex items-center gap-3">
                <div className="h-9 w-9 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-800" />

                <div className="space-y-2">
                  <div className="h-3.5 w-40 animate-pulse rounded bg-slate-100 dark:bg-slate-800" />
                  <div className="h-3 w-20 animate-pulse rounded bg-slate-100 dark:bg-slate-800" />
                </div>
              </div>
            </td>

            <td className="px-5 py-4">
              <div className="h-3.5 w-24 animate-pulse rounded bg-slate-100 dark:bg-slate-800" />
            </td>

            <td className="px-5 py-4">
              <div className="h-3.5 w-20 animate-pulse rounded bg-slate-100 dark:bg-slate-800" />
            </td>

            <td className="px-5 py-4 text-right">
              <div className="ml-auto h-3.5 w-24 animate-pulse rounded bg-slate-100 dark:bg-slate-800" />
            </td>

            <td className="px-5 py-4">
              <div className="ml-auto h-8 w-28 animate-pulse rounded bg-slate-100 dark:bg-slate-800" />
            </td>

            <td className="px-5 py-4">
              <div className="h-7 w-16 animate-pulse rounded-full bg-slate-100 dark:bg-slate-800" />
            </td>

            <td className="px-5 py-4 text-right">
              <div className="ml-auto h-8 w-8 animate-pulse rounded-lg bg-slate-100 dark:bg-slate-800" />
            </td>
          </tr>
        ),
      )}
    </>
  )
}

function EmptyState({
  hasFilters,
  onClear,
  onAddProduct,
}) {
  if (hasFilters) {
    return (
      <div className="flex flex-col items-center justify-center px-6 py-16 text-center">
        <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 text-slate-400 dark:bg-slate-800">
          <SearchX size={22} />
        </div>

        <h3 className="mt-4 text-sm font-semibold text-slate-900 dark:text-slate-100">
          No products found
        </h3>

        <p className="mt-1 max-w-sm text-sm leading-6 text-slate-500">
          Nothing matches your current search
          and filters. Try adjusting your
          selection.
        </p>

        <button
          type="button"
          onClick={onClear}
          className="mt-5 inline-flex h-9 items-center rounded-lg border border-slate-200 bg-white px-3.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
        >
          Clear filters
        </button>
      </div>
    )
  }

  return (
    <div className="flex flex-col items-center justify-center px-6 py-16 text-center">
      <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-slate-100 text-slate-400 dark:bg-slate-800">
        <PackageOpen size={22} />
      </div>

      <h3 className="mt-4 text-sm font-semibold text-slate-900 dark:text-slate-100">
        No products yet
      </h3>

      <p className="mt-1 max-w-sm text-sm leading-6 text-slate-500">
        Add your first product to start
        managing your catalogue and inventory.
      </p>

      <button
        type="button"
        onClick={onAddProduct}
        className="mt-5 inline-flex h-10 items-center rounded-lg bg-slate-950 px-4 text-sm font-semibold text-white transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2"
      >
        Add product
      </button>
    </div>
  )
}

function ProductRow({ product, onEdit }) {
  const initials =
    product.name
      ?.split(' ')
      .slice(0, 2)
      .map((word) => word.charAt(0))
      .join('')
      .toUpperCase() || 'P'

  return (
    <tr className="group transition-colors hover:bg-slate-50/70 dark:hover:bg-slate-800/50">
      {/* Product */}
      <td className="px-5 py-4">
        <div className="flex min-w-[220px] items-center gap-3">
          <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-slate-200 bg-slate-50 text-[11px] font-bold text-slate-500 dark:border-slate-700 dark:bg-slate-800">
            {initials}
          </div>

          <div className="min-w-0">
            <p className="truncate text-sm font-semibold text-slate-900 dark:text-slate-100">
              {product.name}
            </p>

            {product.brand && (
              <p className="mt-0.5 truncate text-xs text-slate-500">
                {product.brand}
              </p>
            )}
          </div>
        </div>
      </td>

      {/* Category */}
      <td className="px-5 py-4">
        <span className="text-sm text-slate-700 dark:text-slate-300">
          {product.category_name ||
            'Uncategorized'}
        </span>
      </td>

      {/* SKU */}
      <td className="px-5 py-4">
        <span className="font-mono text-xs text-slate-500">
          {product.sku || '—'}
        </span>
      </td>

      {/* Selling price */}
      <td className="px-5 py-4 text-right">
        <span className="whitespace-nowrap text-sm font-semibold tabular-nums text-slate-900 dark:text-slate-100">
          {formatCurrency(
            product.selling_price,
          )}
        </span>

        <span className="ml-1 text-xs text-slate-400">
          / {String(
            product.unit || 'unit',
          ).toLowerCase()}
        </span>
      </td>

      {/* Stock */}
      <td className="px-5 py-4">
        <StockIndicator product={product} />
      </td>

      {/* Status */}
      <td className="px-5 py-4">
        <StatusBadge
          active={Boolean(product.is_active)}
        />
      </td>

      {/* Action */}
      <td className="px-5 py-4 text-right">
        <button
          type="button"
          onClick={() => onEdit(product)}
          aria-label={`Edit ${product.name}`}
          title="Edit product"
          className="inline-flex h-8 w-8 items-center justify-center rounded-lg text-slate-400 opacity-70 transition hover:bg-white hover:text-slate-800 hover:shadow-sm group-hover:opacity-100 focus:opacity-100 focus:outline-none focus:ring-2 focus:ring-slate-400 dark:hover:bg-slate-800 dark:hover:text-slate-200"
        >
          <Edit3 size={15} />
        </button>
      </td>
    </tr>
  )
}

export default function ProductTable({
  products,
  loading,
  hasFilters,
  onClear,
  onEdit,
  onAddProduct,
}) {
  return (
    <section className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-sm dark:border-slate-700 dark:bg-slate-900">
      {/* Table heading */}
      <div className="flex items-center justify-between border-b border-slate-100 px-5 py-4 dark:border-slate-800">
        <div>
          <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
            Product catalogue
          </h2>

          <p className="mt-0.5 text-xs text-slate-500">
            {loading
              ? 'Loading products...'
              : 'Manage products and monitor stock.'}
          </p>
        </div>

        {!loading && products.length > 0 && (
          <span className="text-xs font-medium tabular-nums text-slate-400">
            {products.length}{' '}
            {products.length === 1
              ? 'result'
              : 'results'}
          </span>
        )}
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-[980px] w-full border-collapse">
          <thead>
            <tr className="border-b border-slate-200 bg-slate-50/80 dark:border-slate-700 dark:bg-slate-800/80">
              <th
                scope="col"
                className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-[0.08em] text-slate-400"
              >
                Product
              </th>

              <th
                scope="col"
                className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-[0.08em] text-slate-400"
              >
                Category
              </th>

              <th
                scope="col"
                className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-[0.08em] text-slate-400"
              >
                SKU
              </th>

              <th
                scope="col"
                className="px-5 py-3 text-right text-[11px] font-bold uppercase tracking-[0.08em] text-slate-400"
              >
                Selling price
              </th>

              <th
                scope="col"
                className="px-5 py-3 text-right text-[11px] font-bold uppercase tracking-[0.08em] text-slate-400"
              >
                Stock
              </th>

              <th
                scope="col"
                className="px-5 py-3 text-left text-[11px] font-bold uppercase tracking-[0.08em] text-slate-400"
              >
                Status
              </th>

              <th
                scope="col"
                className="w-16 px-5 py-3"
              >
                <span className="sr-only">
                  Actions
                </span>
              </th>
            </tr>
          </thead>

          <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
            {loading && <LoadingRows />}

            {!loading &&
              products.length === 0 && (
                <tr>
                  <td colSpan={7}>
                    <EmptyState
                      hasFilters={hasFilters}
                      onClear={onClear}
                      onAddProduct={onAddProduct}
                    />
                  </td>
                </tr>
              )}

            {!loading &&
              products.map((product) => (
                <ProductRow
                  key={product.id}
                  product={product}
                  onEdit={onEdit}
                />
              ))}
          </tbody>
        </table>
      </div>

      {/* Footer */}
      {!loading && products.length > 0 && (
        <div className="flex items-center justify-between border-t border-slate-100 px-5 py-3 dark:border-slate-800">
          <p className="text-xs text-slate-500">
            Showing{' '}
            <span className="font-semibold text-slate-700 dark:text-slate-300">
              {products.length}
            </span>{' '}
            {products.length === 1
              ? 'product'
              : 'products'}
          </p>

          <p className="text-xs text-slate-400">
            Product catalogue
          </p>
        </div>
      )}
    </section>
  )
}
