import { useState } from 'react'

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

export default function CategoryForm({
  loading = false,
  error = '',
  onSubmit,
  onClose,
}) {
  const [name, setName] = useState('')
  const [group, setGroup] = useState(
    'ALCOHOLIC_DRINKS',
  )
  const [description, setDescription] =
    useState('')
  const [localError, setLocalError] =
    useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    setLocalError('')

    const trimmedName = name.trim()

    if (!trimmedName) {
      setLocalError('Category name is required.')
      return
    }

    await onSubmit({
      name: trimmedName,
      group,
      description: description.trim(),
    })
  }

  const formError = localError || error

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/40 p-4">
      <div className="w-full max-w-lg overflow-hidden rounded-2xl bg-white shadow-2xl dark:bg-slate-900">
        <div className="flex items-start justify-between border-b border-slate-100 px-6 py-5 dark:border-slate-800">
          <div>
            <h2 className="text-lg font-semibold text-slate-900 dark:text-slate-100">
              Add Category
            </h2>

            <p className="mt-1 text-sm text-slate-500">
              Create a category for your product catalog.
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

        <form onSubmit={handleSubmit}>
          <div className="space-y-5 p-6">
            {formError && (
              <div
                className="rounded-lg border border-red-100 bg-red-50 px-4 py-3 text-sm text-red-700 dark:border-red-900/50 dark:bg-red-950/30 dark:text-red-300"
                role="alert"
              >
                {formError}
              </div>
            )}

            <label className="block">
              <span className="mb-1.5 block text-sm font-medium text-slate-700 dark:text-slate-300">
                Category name
                <span className="ml-1 text-red-500">
                  *
                </span>
              </span>

              <input
                type="text"
                value={name}
                onChange={(event) =>
                  setName(event.target.value)
                }
                placeholder="e.g. Vodka"
                disabled={loading}
                className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-slate-400 focus:ring-2 focus:ring-slate-100 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
              />
            </label>

            <label className="block">
              <span className="mb-1.5 block text-sm font-medium text-slate-700 dark:text-slate-300">
                Product group
              </span>

              <select
                value={group}
                onChange={(event) =>
                  setGroup(event.target.value)
                }
                disabled={loading}
                className="w-full rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-900 outline-none focus:border-slate-400 focus:ring-2 focus:ring-slate-100 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
              >
                {GROUPS.map((option) => (
                  <option
                    key={option.value}
                    value={option.value}
                  >
                    {option.label}
                  </option>
                ))}
              </select>
            </label>

            <label className="block">
              <span className="mb-1.5 block text-sm font-medium text-slate-700 dark:text-slate-300">
                Description
              </span>

              <textarea
                value={description}
                onChange={(event) =>
                  setDescription(event.target.value)
                }
                rows={3}
                placeholder="Optional description"
                disabled={loading}
                className="w-full resize-none rounded-lg border border-slate-200 bg-white px-3 py-2.5 text-sm text-slate-900 outline-none placeholder:text-slate-400 focus:border-slate-400 focus:ring-2 focus:ring-slate-100 disabled:opacity-50 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200"
              />
            </label>
          </div>

          <div className="flex justify-end gap-3 border-t border-slate-100 px-6 py-4 dark:border-slate-800">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="rounded-lg border border-slate-200 px-4 py-2 text-sm font-medium text-slate-700 hover:bg-slate-50 disabled:opacity-50 dark:border-slate-700 dark:text-slate-200 dark:hover:bg-slate-800"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={loading}
              className="rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50 dark:bg-slate-100 dark:text-slate-900"
            >
              {loading
                ? 'Saving...'
                : 'Create Category'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
