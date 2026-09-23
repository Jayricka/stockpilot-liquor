import {
  Building2,
  ChevronDown,
  Package,
  Plus,
} from 'lucide-react'

function ProductHeader({
  businesses,
  businessId,
  onBusinessChange,
  productCount,
  onAddProduct,
}) {
  const selectedBusiness = businesses.find(
    (business) =>
      String(business.id) === String(businessId),
  )

  return (
    <header className="mb-6">
      <div className="flex flex-col gap-5 xl:flex-row xl:items-end xl:justify-between">
        <div className="flex min-w-0 items-start gap-4">
          <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl border border-slate-200 bg-white text-slate-700 shadow-sm dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200">
            <Package
              size={21}
              strokeWidth={1.8}
            />
          </div>

          <div className="min-w-0">
            <p className="text-xs font-semibold uppercase tracking-[0.12em] text-slate-400">
              Product workspace
            </p>

            <div className="mt-1 flex flex-wrap items-center gap-3">
              <h1 className="text-2xl font-semibold tracking-tight text-slate-950">
                Products
              </h1>

              <span className="rounded-full bg-slate-100 px-2.5 py-1 text-xs font-medium text-slate-600">
                {productCount}{' '}
                {productCount === 1
                  ? 'product'
                  : 'products'}
              </span>
            </div>

            <p className="mt-1.5 max-w-2xl text-sm leading-6 text-slate-500">
              Manage your catalogue, pricing and
              inventory from one workspace.
            </p>
          </div>
        </div>

        <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
          <div className="flex min-w-[220px] items-center gap-3 rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 shadow-sm dark:border-slate-700 dark:bg-slate-800">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-100 text-slate-500">
              <Building2 size={15} />
            </div>

            <div className="min-w-0 flex-1">
              <p className="text-[11px] font-medium uppercase tracking-wide text-slate-400">
                Business
              </p>

              <div className="relative mt-0.5">
                <select
                  value={businessId || ''}
                  onChange={(event) =>
                    onBusinessChange(
                      event.target.value,
                    )
                  }
                  className="w-full appearance-none bg-transparent pr-5 text-sm font-semibold text-slate-800 outline-none"
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

                <ChevronDown
                  size={14}
                  className="pointer-events-none absolute right-0 top-1/2 -translate-y-1/2 text-slate-400"
                />
              </div>
            </div>
          </div>

          <button
            type="button"
            onClick={onAddProduct}
            className="inline-flex h-11 items-center justify-center gap-2 rounded-xl bg-slate-950 px-4 text-sm font-semibold text-white shadow-sm transition hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2"
          >
            <Plus size={17} />
            Add product
          </button>
        </div>
      </div>

      {selectedBusiness && (
        <div className="mt-4 flex items-center gap-2 text-xs text-slate-400 xl:hidden">
          <Building2 size={13} />
          <span>{selectedBusiness.name}</span>
        </div>
      )}
    </header>
  )
}

export default ProductHeader
