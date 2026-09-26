export default function ProductFormFields({
  form,
  updateField,
  Field,
  inputClass,
  UNITS,
}) {
  return (
    <section>
      <h3 className="mb-4 text-sm font-semibold text-slate-900 dark:text-slate-100">
        Product details
      </h3>

      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Product Name" required>
          <input
            value={form.name}
            onChange={(e) => updateField('name', e.target.value)}
            placeholder="e.g. Vodka 750ml"
            className={inputClass}
          />
        </Field>

        <Field label="Brand">
          <input
            value={form.brand}
            onChange={(e) => updateField('brand', e.target.value)}
            placeholder="e.g. Smirnoff"
            className={inputClass}
          />
        </Field>

        <Field label="SKU">
          <input
            value={form.sku}
            onChange={(e) => updateField('sku', e.target.value)}
            placeholder="e.g. SMIRNOFF-750"
            className={inputClass}
          />
        </Field>

        <Field label="Unit" required>
          <select
            value={form.unit}
            onChange={(e) => updateField('unit', e.target.value)}
            className={inputClass}
          >
            {UNITS.map((unit) => (
              <option key={unit.value} value={unit.value}>
                {unit.label}
              </option>
            ))}
          </select>
        </Field>
      </div>
    </section>
  )
}
