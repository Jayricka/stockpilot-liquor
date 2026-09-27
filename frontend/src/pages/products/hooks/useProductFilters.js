import { useMemo, useState } from 'react'

const CATALOG_GROUPS = [
  {
    value: 'all',
    label: 'All products',
    countKey: 'all',
  },
  {
    value: 'ALCOHOLIC_DRINKS',
    label: 'Alcoholic Drinks',
    countKey: 'ALCOHOLIC_DRINKS',
  },
  {
    value: 'SODA_AND_DRINKS',
    label: 'Soda & Drinks',
    countKey: 'SODA_AND_DRINKS',
  },
  {
    value: 'CIGARETTES_AND_TOBACCO',
    label: 'Cigarettes & Tobacco',
    countKey: 'CIGARETTES_AND_TOBACCO',
  },
  {
    value: 'OTHER',
    label: 'Other',
    countKey: 'OTHER',
  },
]

function getCategoryId(product) {
  if (
    product?.category &&
    typeof product.category === 'object'
  ) {
    return product.category.id || ''
  }

  return (
    product?.category_id ||
    product?.category ||
    ''
  )
}

function getCategoryGroup(product) {
  if (product?.category_group) {
    return product.category_group
  }

  if (
    product?.category &&
    typeof product.category === 'object'
  ) {
    return (
      product.category.group ||
      product.category.category_group ||
      ''
    )
  }

  return ''
}

export function useProductFilters(products, categories) {
  const [search, setSearch] = useState('')
  const [catalogFilter, setCatalogFilter] =
    useState('all')
  const [categoryFilter, setCategoryFilter] =
    useState('all')
  const [stockFilter, setStockFilter] =
    useState('all')
  const [statusFilter, setStatusFilter] =
    useState('all')

  const filteredCategories = useMemo(() => {
    if (catalogFilter === 'all') {
      return categories
    }

    return categories.filter(
      (category) =>
        String(category.group) ===
        String(catalogFilter),
    )
  }, [categories, catalogFilter])

  const catalogCounts = useMemo(() => {
    const counts = {
      all: products.length,
      ALCOHOLIC_DRINKS: 0,
      SODA_AND_DRINKS: 0,
      CIGARETTES_AND_TOBACCO: 0,
      OTHER: 0,
    }

    products.forEach((product) => {
      const group = getCategoryGroup(product)

      if (
        Object.prototype.hasOwnProperty.call(
          counts,
          group,
        )
      ) {
        counts[group] += 1
      }
    })

    return counts
  }, [products])

  const filteredProducts = useMemo(() => {
    const query = search.trim().toLowerCase()

    return products.filter((product) => {
      const name = String(
        product.name || '',
      ).toLowerCase()

      const brand = String(
        product.brand || '',
      ).toLowerCase()

      const category = String(
        product.category_name || '',
      ).toLowerCase()

      const sku = String(
        product.sku || '',
      ).toLowerCase()

      const group = getCategoryGroup(product)
      const categoryId = getCategoryId(product)

      const stock = Number(
        product.stock_quantity || 0,
      )

      const matchesSearch =
        !query ||
        name.includes(query) ||
        brand.includes(query) ||
        category.includes(query) ||
        sku.includes(query)

      const matchesCatalog =
        catalogFilter === 'all' ||
        String(group) === String(catalogFilter)

      const matchesCategory =
        categoryFilter === 'all' ||
        String(categoryId) ===
          String(categoryFilter)

      let matchesStock = true

      if (stockFilter === 'in-stock') {
        matchesStock = stock > 0
      }

      if (stockFilter === 'low-stock') {
        matchesStock = Boolean(
          product.is_low_stock,
        )
      }

      if (stockFilter === 'out-of-stock') {
        matchesStock = stock <= 0
      }

      let matchesStatus = true

      if (statusFilter === 'active') {
        matchesStatus = Boolean(
          product.is_active,
        )
      }

      if (statusFilter === 'inactive') {
        matchesStatus = !product.is_active
      }

      return (
        matchesSearch &&
        matchesCatalog &&
        matchesCategory &&
        matchesStock &&
        matchesStatus
      )
    })
  }, [
    products,
    search,
    catalogFilter,
    categoryFilter,
    stockFilter,
    statusFilter,
  ])

  const hasActiveFilters =
    Boolean(search.trim()) ||
    catalogFilter !== 'all' ||
    categoryFilter !== 'all' ||
    stockFilter !== 'all' ||
    statusFilter !== 'all'

  function resetFilters() {
    setSearch('')
    setCatalogFilter('all')
    setCategoryFilter('all')
    setStockFilter('all')
    setStatusFilter('all')
  }

  function handleCatalogChange(value) {
    setCatalogFilter(value)
    setCategoryFilter('all')
  }

  return {
    search,
    setSearch,
    catalogFilter,
    categoryFilter,
    stockFilter,
    statusFilter,
    setCategoryFilter,
    setStockFilter,
    setStatusFilter,
    catalogGroups: CATALOG_GROUPS,
    catalogCounts,
    filteredCategories,
    filteredProducts,
    hasActiveFilters,
    resetFilters,
    handleCatalogChange,
  }
}
