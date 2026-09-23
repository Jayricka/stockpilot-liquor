import { useMemo, useState } from 'react'

function ProductGrid({
  products,
  search,
  loading,
  onAdd,
}) {
  const [category, setCategory] =
    useState('ALL')

  const categories = useMemo(() => {
    const values = products
      .map(
        (product) =>
          product.category_name ||
          product.category?.name,
      )
      .filter(Boolean)

    return ['ALL', ...new Set(values)]
  }, [products])

  const query = search
    .trim()
    .toLowerCase()

  const filteredProducts =
    products.filter((product) => {
      const name = String(
        product.name || '',
      ).toLowerCase()

      const brand = String(
        product.brand || '',
      ).toLowerCase()

      const sku = String(
        product.sku || '',
      ).toLowerCase()

      const productCategory =
        product.category_name ||
        product.category?.name ||
        ''

      const matchesSearch =
        !query ||
        name.includes(query) ||
        brand.includes(query) ||
        sku.includes(query)

      const matchesCategory =
        category === 'ALL' ||
        productCategory === category

      return (
        matchesSearch &&
        matchesCategory
      )
    })

  if (loading) {
    return (
      <div className="product-grid-empty">
        Loading products...
      </div>
    )
  }

  return (
    <>
      <div className="product-categories">
        {categories.map((item) => (
          <button
            key={item}
            type="button"
            className={
              category === item
                ? 'category-filter active'
                : 'category-filter'
            }
            onClick={() =>
              setCategory(item)
            }
          >
            {item === 'ALL'
              ? 'All'
              : item}
          </button>
        ))}
      </div>

      {!filteredProducts.length ? (
        <div className="product-grid-empty">
          <h3>No products found</h3>
          <p>
            Try another search or category.
          </p>
        </div>
      ) : (
        <div className="product-grid">
          {filteredProducts.map(
            (product) => {
              const stock = Number(
                product.stock_quantity || 0,
              )

              const disabled = stock <= 0

              return (
                <button
                  key={product.id}
                  type="button"
                  className="product-card"
                  disabled={disabled}
                  onClick={() =>
                    onAdd(product)
                  }
                >
                  <div className="product-card-top">
                    <span>
                      {product.category_name ||
                        product.category?.name ||
                        'Product'}
                    </span>

                    <strong>
                      {stock}
                    </strong>
                  </div>

                  <div className="product-card-body">
                    <h3>
                      {product.name}
                    </h3>

                    {product.brand && (
                      <p>
                        {product.brand}
                      </p>
                    )}

                    <small>
                      {product.sku ||
                        'No SKU'}
                    </small>
                  </div>

                  <div className="product-card-footer">
                    <strong>
                      KES{' '}
                      {Number(
                        product.selling_price ||
                          0,
                      ).toLocaleString()}
                    </strong>

                    <span>
                      {disabled
                        ? 'Out of stock'
                        : `Add · ${
                            product.unit ||
                            'unit'
                          }`}
                    </span>
                  </div>
                </button>
              )
            },
          )}
        </div>
      )}
    </>
  )
}

export default ProductGrid
