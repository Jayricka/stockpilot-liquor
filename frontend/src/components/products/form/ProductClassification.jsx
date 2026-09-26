export default function ProductClassification({
  form,
  updateField,
  changeGroup,
  filteredCategories,
  GROUPS,
  Field,
  inputClass,
}) {
  return (
    <section>
      <h3 className="mb-4 text-sm font-semibold text-slate-900 dark:text-slate-100">
        Classification
      </h3>

      <div className="grid gap-4 sm:grid-cols-2">
        <Field label="Catalog" required>
          <select
            value={form.group}
            onChange={(event) =>
              changeGroup(event.target.value)
            }
            className={inputClass}
          >
            <option value="">Select catalog</option>

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

        <Field label="Category" required>
          <select
            value={form.category}
            onChange={(event) =>
              updateField(
                'category',
                event.target.value,
              )
            }
            className={inputClass}
          >
            <option value="">
              {form.group
                ? 'Select category'
                : 'Select catalog first'}
            </option>

            {filteredCategories.map((category) => (
              <option
                key={category.id}
                value={category.id}
              >
                {category.name}
              </option>
            ))}
          </select>
        </Field>
      </div>
    </section>
  )
}
