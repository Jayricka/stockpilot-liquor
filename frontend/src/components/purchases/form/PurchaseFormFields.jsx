function PurchaseFormFields({
  suppliers,
  form,
  onChange,
}) {
  return (
    <div className="purchase-form-grid">
      <label>
        Supplier
        <select
          name="supplier"
          value={form.supplier}
          onChange={onChange}
          required
        >
          <option value="">
            Select supplier
          </option>

          {suppliers.map((supplier) => (
            <option
              key={supplier.id}
              value={supplier.id}
            >
              {supplier.name}
            </option>
          ))}
        </select>
      </label>

      <label>
        Reference number
        <input
          name="reference_number"
          value={form.reference_number}
          onChange={onChange}
          placeholder="e.g. PO-00021"
          required
        />
      </label>

      <label>
        Purchase date
        <input
          type="date"
          name="purchase_date"
          value={form.purchase_date}
          onChange={onChange}
          required
        />
      </label>
    </div>
  )
}

export default PurchaseFormFields
