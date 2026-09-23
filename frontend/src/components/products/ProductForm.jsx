import { useMemo, useState } from 'react'

const GROUPS = [
  { value: 'ALCOHOLIC_DRINKS', label: 'Alcoholic Drinks' },
  { value: 'SODA_AND_DRINKS', label: 'Soda & Drinks' },
  { value: 'CIGARETTES_AND_TOBACCO', label: 'Cigarettes & Tobacco' },
  { value: 'OTHER', label: 'Other' },
]

const UNITS = [
  { value: 'BOTTLE', label: 'Bottle' },
  { value: 'LITRE', label: 'Litre' },
  { value: 'CRATE', label: 'Crate' },
  { value: 'PIECE', label: 'Piece' },
]

const EMPTY_FORM = {
  group: '',
  category: '',
  brand: '',
  name: '',
  sku: '',
  unit: 'BOTTLE',
  buying_price: '',
  selling_price: '',
  initial_quantity: '0',
  reorder_level: '0',
  is_active: true,
}

function getInitialForm(product) {
  if (!product) return EMPTY_FORM

  const category =
    typeof product.category === 'object'
      ? product.category
      : null

  return {
    group:
      product.category_group ||
      category?.group ||
      '',
    category: String(
      category?.id ||
        product.category_id ||
        product.category ||
        '',
    ),
    brand: product.brand || '',
    name: product.name || '',
    sku: product.sku || '',
    unit: product.unit || 'BOTTLE',
    buying_price: String(
      product.buying_price ?? '',
    ),
    selling_price: String(
      product.selling_price ?? '',
    ),
    initial_quantity: '0',
    reorder_level: String(
      product.reorder_level ?? '0',
    ),
    is_active: product.is_active ?? true,
  }
}

const inputClass =
  'w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-slate-400 focus:ring-2 focus:ring-slate-100 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:placeholder:text-slate-500 dark:focus:border-slate-600 dark:focus:ring-slate-700'

function Field({
  label,
  required,
  children,
}) {
  return (
    <label className="block">
      <span className="mb-1.5 block text-sm font-medium text-slate-700 dark:text-slate-300">
        {label}

        {required && (
          <span className="ml-1 text-red-500">
            *
          </span>
        )}
      </span>

      {children}
    </label>
  )
}

export default function ProductForm({
  categories = [],
  product = null,
  loading = false,
  error = '',
  onSubmit,
  onClose,
}) {
  const editing = Boolean(product)

  const [form, setForm] = useState(() =>
    getInitialForm(product),
  )

  const [localError, setLocalError] =
    useState('')

  const filteredCategories = useMemo(
    () =>
      categories.filter(
        (category) =>
          category.group === form.group,
      ),
    [categories, form.group],
  )

  function updateField(name, value) {
    setForm((current) => ({
      ...current,
      [name]: value,
    }))
  }

  function changeGroup(value) {
    setForm((current) => ({
      ...current,
      group: value,
      category: '',
    }))
  }

  function validate() {
    if (!form.group) {
      return 'Please select a product group.'
    }

    if (!form.category) {
      return 'Please select a category.'
    }

    if (!form.name.trim()) {
      return 'Product name is required.'
    }

    if (
      form.buying_price === '' ||
      Number(form.buying_price) < 0
    ) {
      return 'Buying price must be zero or greater.'
    }

    if (
      form.selling_price === '' ||
      Number(form.selling_price) < 0
    ) {
      return 'Selling price must be zero or greater.'
    }

    if (
      Number(form.selling_price) <
      Number(form.buying_price)
    ) {
      return 'Selling price cannot be lower than buying price.'
    }

    if (
      form.reorder_level === '' ||
      Number(form.reorder_level) < 0
    ) {
      return 'Reorder level must be zero or greater.'
    }

    if (
      !editing &&
      (form.initial_quantity === '' ||
        Number(form.initial_quantity) < 0)
    ) {
      return 'Opening quantity must be zero or greater.'
    }

    return ''
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setLocalError('')

    const validationError = validate()

    if (validationError) {
      setLocalError(validationError)
      return
    }

    const payload = {
      category: Number(form.category),
      brand: form.brand.trim(),
      name: form.name.trim(),
      sku: form.sku.trim(),
      unit: form.unit,
      buying_price: form.buying_price,
      selling_price: form.selling_price,
      reorder_level: form.reorder_level,
      is_active: form.is_active,
    }

    if (!editing) {
      payload.initial_quantity =
        form.initial_quantity || '0'
    }

    await onSubmit(payload)
  }

  const formError = localError || error

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4">
      <div className="flex max-h-[92vh] w-full max-w-2xl flex-col overflow-hidden rounded-2xl bg-white shadow-2xl dark:bg-slate-900">
        <div className="flex items-start justify-between border-b border-slate-100 px-6 py-5 dark:border-slate-800">
          <div>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
              {editing
                ? 'Edit Product'
                : 'Add Product'}
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              {editing
                ? 'Update product details without changing stock.'
                : 'Create a product and optionally set its opening stock.'}
            </p>
          </div>

          <button
            type="button"
            onClick={onClose}
            disabled={loading}
            className="rounded-lg p-2 text-2xl leading-none text-slate-400 hover:bg-slate-100 hover:text-slate-700 disabled:opacity-50 dark:hover:bg-slate-800 dark:hover:text-slate-200"
            aria-label="Close"
          >
            ×
          </button>
        </div>

        <form
          id="product-form"
          onSubmit={handleSubmit}
          className="overflow-y-auto"
        >
          <div className="space-y-6 p-6">
            {formError && (
              <div className="rounded-lg border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-300">
                {typeof formError === 'string'
                  ? formError
                  : 'Unable to save product. Please check the form.'}
              </div>
            )}

            <section>
              <h3 className="mb-4 text-sm font-semibold text-slate-900 dark:text-slate-100">
                Product details
              </h3>

              <div className="grid gap-4 sm:grid-cols-2">
                <Field
                  label="Product Name"
                  required
                >
                  <input
                    value={form.name}
                    onChange={(e) =>
                      updateField(
                        'name',
                        e.target.value,
                      )
                    }
                    placeholder="e.g. Vodka 750ml"
                    className={inputClass}
                  />
                </Field>

                <Field label="Brand">
                  <input
                    value={form.brand}
                    onChange={(e) =>
                      updateField(
                        'brand',
                        e.target.value,
                      )
                    }
                    placeholder="e.g. Smirnoff"
                    className={inputClass}
                  />
                </Field>

                <Field label="SKU">
                  <input
                    value={form.sku}
                    onChange={(e) =>
                      updateField(
                        'sku',
                        e.target.value,
                      )
                    }
                    placeholder="e.g. SMIRNOFF-750"
                    className={inputClass}
                  />
                </Field>

                <Field label="Unit" required>
                  <select
                    value={form.unit}
                    onChange={(e) =>
                      updateField(
                        'unit',
                        e.target.value,
                      )
                    }
                    className={inputClass}
                  >
                    {UNITS.map((unit) => (
                      <option
                        key={unit.value}
                        value={unit.value}
                      >
                        {unit.label}
                      </option>
                    ))}
                  </select>
                </Field>
              </div>
            </section>

            <section>
              <h3 className="mb-4 text-sm font-semibold text-slate-900 dark:text-slate-100">
                Classification
              </h3>

              <div className="grid gap-4 sm:grid-cols-2">
                <Field
                  label="Catalog"
                  required
                >
                  <select
                    value={form.group}
                    onChange={(e) =>
                      changeGroup(
                        e.target.value,
                      )
                    }
                    className={inputClass}
                  >
                    <option value="">
                      Select catalog
                    </option>

                    {GROUPS.map((group) => (
                      <option
                        key={group.value}
                        value={group.value}
                      >
                        {group.label}
                      </option>
                    ))}
                  </select>
                </Field>

                <Field
                  label="Category"
                  required
                >
                  <select
                    value={form.category}
                    onChange={(e) =>
                      updateField(
                        'category',
                        e.target.value,
                      )
                    }
                    disabled={!form.group}
                    className={`${inputClass} disabled:cursor-not-allowed disabled:bg-slate-50 dark:disabled:bg-slate-900`}
                  >
                    <option value="">
                      {form.group
                        ? 'Select category'
                        : 'Select catalog first'}
                    </option>

                    {filteredCategories.map(
                      (category) => (
                        <option
                          key={category.id}
                          value={category.id}
                        >
                          {category.name}
                        </option>
                      ),
                    )}
                  </select>
                </Field>
              </div>
            </section>

            <section>
              <h3 className="mb-4 text-sm font-semibold text-slate-900 dark:text-slate-100">
                Pricing
              </h3>

              <div className="grid gap-4 sm:grid-cols-2">
                <Field
                  label="Buying Price"
                  required
                >
                  <div className="relative">
                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
                      KES
                    </span>

                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={
                        form.buying_price
                      }
                      onChange={(e) =>
                        updateField(
                          'buying_price',
                          e.target.value,
                        )
                      }
                      placeholder="0.00"
                      className={`${inputClass} pl-12`}
                    />
                  </div>
                </Field>

                <Field
                  label="Selling Price"
                  required
                >
                  <div className="relative">
                    <span className="absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
                      KES
                    </span>

                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={
                        form.selling_price
                      }
                      onChange={(e) =>
                        updateField(
                          'selling_price',
                          e.target.value,
                        )
                      }
                      placeholder="0.00"
                      className={`${inputClass} pl-12`}
                    />
                  </div>
                </Field>
              </div>
            </section>

            <section>
              <h3 className="mb-4 text-sm font-semibold text-slate-900 dark:text-slate-100">
                Inventory
              </h3>

              <div className="grid gap-4 sm:grid-cols-2">
                {editing ? (
                  <Field label="Current Stock">
                    <div
                      className={`${inputClass} bg-slate-50 text-slate-600 dark:bg-slate-800 dark:text-slate-300`}
                    >
                      {Number(
                        product.stock_quantity ||
                          0,
                      ).toLocaleString('en-KE', {
                        maximumFractionDigits: 2,
                      })}{' '}
                      {UNITS.find(
                        (unit) =>
                          unit.value ===
                          product.unit,
                      )?.label ||
                        product.unit}
                    </div>

                    <p className="mt-1.5 text-xs text-slate-500">
                      Stock is managed through
                      inventory operations.
                    </p>
                  </Field>
                ) : (
                  <Field label="Opening Quantity">
                    <input
                      type="number"
                      min="0"
                      step="0.01"
                      value={
                        form.initial_quantity
                      }
                      onChange={(e) =>
                        updateField(
                          'initial_quantity',
                          e.target.value,
                        )
                      }
                      className={inputClass}
                    />

                    <p className="mt-1.5 text-xs text-slate-500">
                      Optional starting stock.
                    </p>
                  </Field>
                )}

                <Field label="Reorder Level">
                  <input
                    type="number"
                    min="0"
                    step="0.01"
                    value={
                      form.reorder_level
                    }
                    onChange={(e) =>
                      updateField(
                        'reorder_level',
                        e.target.value,
                      )
                    }
                    className={inputClass}
                  />

                  <p className="mt-1.5 text-xs text-slate-500">
                    Alert when stock reaches
                    this level.
                  </p>
                </Field>
              </div>
            </section>

            <section>
              <h3 className="mb-3 text-sm font-semibold text-slate-900 dark:text-slate-100">
                Product Status
              </h3>

              <label className="flex cursor-pointer gap-3 rounded-lg border border-slate-200 p-4 dark:border-slate-700">
                <input
                  type="checkbox"
                  checked={form.is_active}
                  onChange={(e) =>
                    updateField(
                      'is_active',
                      e.target.checked,
                    )
                  }
                  className="mt-1 h-4 w-4 rounded border-slate-300"
                />

                <span>
                  <span className="block text-sm font-medium text-slate-800 dark:text-slate-200">
                    Active
                  </span>

                  <span className="mt-1 block text-xs text-slate-500">
                    Inactive products remain in
                    historical records but cannot
                    be used for new operational
                    transactions.
                  </span>
                </span>
              </label>
            </section>
          </div>

          <div className="flex justify-end gap-3 border-t border-slate-100 bg-slate-50/70 px-6 py-4 dark:border-slate-800 dark:bg-slate-950/40">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="rounded-lg border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={loading}
              className="rounded-lg bg-slate-900 px-5 py-2.5 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-white"
            >
              {loading
                ? 'Saving...'
                : editing
                  ? 'Save Changes'
                  : 'Create Product'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
