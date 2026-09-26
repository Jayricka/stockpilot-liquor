export default function ProductInventory({
  form,
  updateField,
  editing,
  product,
  UNITS,
  Field,
  inputClass,
}) {
  return (
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
              {Number(product.stock_quantity || 0).toLocaleString('en-KE', {
                maximumFractionDigits: 2,
              })}{' '}
              {UNITS.find((unit) => unit.value === product.unit)?.label ||
                product.unit}
            </div>

            <p className="mt-1.5 text-xs text-slate-500">
              Stock is managed through inventory operations.
            </p>
          </Field>
        ) : (
          <Field label="Opening Quantity">
            <input
              type="number"
              min="0"
              step="0.01"
              value={form.initial_quantity}
              onChange={(e) =>
                updateField('initial_quantity', e.target.value)
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
            value={form.reorder_level}
            onChange={(e) =>
              updateField('reorder_level', e.target.value)
            }
            className={inputClass}
          />

          <p className="mt-1.5 text-xs text-slate-500">
            Alert when stock reaches this level.
          </p>
        </Field>
      </div>
    </section>
  )
}
