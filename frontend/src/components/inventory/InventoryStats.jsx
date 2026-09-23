function InventoryStats({ products }) {
  const lowStockCount = products.filter(
    (product) =>
      Number(product.stock_quantity) <=
      Number(product.reorder_level),
  ).length

  const totalStock = products.reduce(
    (total, product) =>
      total + Number(product.stock_quantity || 0),
    0,
  )

  const stockValue = products.reduce(
    (total, product) =>
      total +
      Number(product.stock_quantity || 0) *
        Number(product.buying_price || 0),
    0,
  )

  const stats = [
    {
      label: 'Products',
      value: products.length,
    },
    {
      label: 'Total units',
      value: totalStock.toLocaleString(),
    },
    {
      label: 'Low stock',
      value: lowStockCount,
    },
    {
      label: 'Stock value',
      value: `KES ${stockValue.toLocaleString()}`,
    },
  ]

  return (
    <div className="inventory-stats">
      {stats.map((stat) => (
        <article className="inventory-stat" key={stat.label}>
          <span>{stat.label}</span>
          <strong>{stat.value}</strong>
        </article>
      ))}
    </div>
  )
}

export default InventoryStats
