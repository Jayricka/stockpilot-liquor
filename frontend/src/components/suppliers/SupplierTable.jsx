function SupplierTable({
  suppliers,
  onEdit,
  onDelete,
}) {
  return (
    <div className="suppliers-table-wrap">
      <table className="suppliers-table">
        <thead>
          <tr>
            <th scope="col">
              Supplier
            </th>

            <th scope="col">
              Contact
            </th>

            <th scope="col">
              Address
            </th>

            <th scope="col">
              Status
            </th>

            <th scope="col">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {suppliers.map((supplier) => (
            <tr key={supplier.id}>
              <td>
                <strong>
                  {supplier.name}
                </strong>

                {supplier.notes && (
                  <small>
                    {supplier.notes}
                  </small>
                )}
              </td>

              <td>
                <strong>
                  {supplier.phone ||
                    'No phone'}
                </strong>

                <small>
                  {supplier.email ||
                    'No email'}
                </small>
              </td>

              <td>
                {supplier.address || '—'}
              </td>

              <td>
                <span
                  className={
                    supplier.is_active
                      ? 'supplier-status active'
                      : 'supplier-status'
                  }
                >
                  {supplier.is_active
                    ? 'Active'
                    : 'Inactive'}
                </span>
              </td>

              <td>
                <div className="supplier-row-actions">
                  <button
                    type="button"
                    onClick={() =>
                      onEdit(supplier)
                    }
                  >
                    Edit
                  </button>

                  <button
                    type="button"
                    onClick={() =>
                      onDelete(supplier)
                    }
                  >
                    Delete
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default SupplierTable
