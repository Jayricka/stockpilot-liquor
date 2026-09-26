export default function ProductStatus({
  form,
  updateField,
}) {
  return (
    <section>
      <h3 className="mb-3 text-sm font-semibold text-slate-900 dark:text-slate-100">
        Product Status
      </h3>

      <label className="flex cursor-pointer gap-3 rounded-lg border border-slate-200 p-4 dark:border-slate-700">
        <input
          type="checkbox"
          checked={form.is_active}
          onChange={(e) => updateField('is_active', e.target.checked)}
          className="mt-1 h-4 w-4 rounded border-slate-300"
        />

        <span>
          <span className="block text-sm font-medium text-slate-800 dark:text-slate-200">
            Active
          </span>

          <span className="mt-1 block text-xs text-slate-500">
            Inactive products remain in historical records but cannot be used
            for new operational transactions.
          </span>
        </span>
      </label>
    </section>
  )
}
