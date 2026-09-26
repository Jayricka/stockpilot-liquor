import { useMemo, useState } from 'react'

import ProductClassification from './ProductClassification'
import ProductFormFields from './ProductFormFields'
import ProductInventory from './ProductInventory'
import ProductPricing from './ProductPricing'
import ProductStatus from './ProductStatus'

const GROUPS = [
  {
    value: 'ALCOHOLIC_DRINKS',
    label: 'Alcoholic Drinks',
  },
  {
    value: 'SODA_AND_DRINKS',
    label: 'Soda & Drinks',
  },
  {
    value: 'CIGARETTES_AND_TOBACCO',
    label: 'Cigarettes & Tobacco',
  },
  {
    value: 'OTHER',
    label: 'Other',
  },
]

const UNITS = [
  {
    value: 'BOTTLE',
    label: 'Bottle',
  },
  {
    value: 'LITRE',
    label: 'Litre',
  },
  {
    value: 'CRATE',
    label: 'Crate',
  },
  {
    value: 'PIECE',
    label: 'Piece',
  },
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
  if (!product) {
    return EMPTY_FORM
  }

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

  const [form, setForm] = useState(
    () => getInitialForm(product),
  )
  const [localError, setLocalError] = useState('')

  const filteredCategories = useMemo(() => {
    if (!form.group) {
      return []
    }

    return categories.filter((category) => {
      const categoryGroup =
        category.group ||
        category.category_group ||
        ''

      return (
        String(categoryGroup).trim() ===
        String(form.group).trim()
      )
    })
  }, [categories, form.group])

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
      (
        form.initial_quantity === '' ||
        Number(form.initial_quantity) < 0
      )
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

            <ProductFormFields
              form={form}
              updateField={updateField}
              Field={Field}
              inputClass={inputClass}
              UNITS={UNITS}
            />

            <ProductClassification
              form={form}
              updateField={updateField}
              changeGroup={changeGroup}
              filteredCategories={filteredCategories}
              GROUPS={GROUPS}
              Field={Field}
              inputClass={inputClass}
            />

            <ProductPricing
              form={form}
              updateField={updateField}
              Field={Field}
              inputClass={inputClass}
            />

            <ProductInventory
              form={form}
              updateField={updateField}
              editing={editing}
              product={product}
              UNITS={UNITS}
              Field={Field}
              inputClass={inputClass}
            />

            <ProductStatus
              form={form}
              updateField={updateField}
              Field={Field}
              inputClass={inputClass}
            />
          </div>

          <div className="flex justify-end gap-3 border-t border-slate-100 px-6 py-4 dark:border-slate-800">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50 disabled:opacity-50 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={loading}
              className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-slate-100 dark:text-slate-900 dark:hover:bg-white"
            >
              {loading
                ? 'Saving...'
                : editing
                  ? 'Update Product'
                  : 'Create Product'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
