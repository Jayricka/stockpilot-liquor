export default function ProductPricing({
  form,
  updateField,
  Field,
  inputClass,
}) {
  return (
    <section>
      <h3 className="mb-4 text-sm font-semibold text-slate-900 dark:text-slate-100">
        Pricing
      </h3>

      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Buying Price" required>
          <div className="relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
              KES
            </span>

            <input
              type="number"
              min="0"
              step="0.01"
              value={form.buying_price}
              onChange={(e) =>
                updateField('buying_price', e.target.value)
              }
              placeholder="0.00"
              className={`${inputClass} pl-12`}
            />
          </div>
        </Field>

        <Field label="Selling Price" required>
          <div className="relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-xs text-slate-400">
              KES
            </span>

            <input
              type="number"
              min="0"
              step="0.01"
              value={form.selling_price}
              onChange={(e) =>
                updateField('selling_price', e.target.value)
              }
              placeholder="0.00"
              className={`${inputClass} pl-12`}
            />
          </div>
        </Field>
      </div>
    </section>
  )
}
