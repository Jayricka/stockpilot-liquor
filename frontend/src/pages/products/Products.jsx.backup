/* eslint-disable react-hooks/set-state-in-effect */

import {
  useCallback,
  useEffect,
  useMemo,
  useState,
} from 'react'

import ProductFilters from '../../components/products/ProductFilters'
import ProductForm from '../../components/products/ProductForm'
import ProductHeader from '../../components/products/ProductHeader'
import ProductLoading from '../../components/products/ProductLoading'
import ProductStats from '../../components/products/ProductStats'
import ProductTable from '../../components/products/ProductTable'

import {
  createProduct,
  getCategories,
  getProducts,
  updateProduct,
} from '../../services/products'

import { getBusinesses } from '../../services/dashboard'

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

function getErrorMessage(error) {
  const data = error?.response?.data

  if (!data) {
    return 'Something went wrong. Please try again.'
  }

  if (typeof data.detail === 'string') {
    return data.detail
  }

  if (Array.isArray(data.detail)) {
    return data.detail.join(', ')
  }

  if (Array.isArray(data.non_field_errors)) {
    return data.non_field_errors.join(', ')
  }

  const firstError = Object.values(data)[0]

  if (Array.isArray(firstError)) {
    return firstError.join(', ')
  }

  if (typeof firstError === 'string') {
    return firstError
  }

  return 'Something went wrong. Please try again.'
}

function normalizeList(data) {
  if (Array.isArray(data)) {
    return data
  }

  return data?.results || []
}

function Products() {
  const [businesses, setBusinesses] = useState([])
  const [businessId, setBusinessId] = useState('')

  const [products, setProducts] = useState([])
  const [categories, setCategories] = useState([])

  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  const [search, setSearch] = useState('')
  const [catalogFilter, setCatalogFilter] =
    useState('all')
  const [categoryFilter, setCategoryFilter] =
    useState('all')
  const [stockFilter, setStockFilter] =
    useState('all')
  const [statusFilter, setStatusFilter] =
    useState('all')

  const [formOpen, setFormOpen] = useState(false)
  const [editingProduct, setEditingProduct] =
    useState(null)

  const loadBusinesses = useCallback(async () => {
    try {
      const data = await getBusinesses()
      const list = normalizeList(data)

      setBusinesses(list)

      if (list.length && !businessId) {
        setBusinessId(String(list[0].id))
      }
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    }
  }, [businessId])

  const loadWorkspaceData = useCallback(
    async (selectedBusinessId) => {
      if (!selectedBusinessId) {
        setProducts([])
        setCategories([])
        setLoading(false)
        return
      }

      try {
        setLoading(true)
        setError('')

        const [
          productsData,
          categoriesData,
        ] = await Promise.all([
          getProducts(selectedBusinessId),
          getCategories(selectedBusinessId),
        ])

        setProducts(normalizeList(productsData))
        setCategories(normalizeList(categoriesData))
      } catch (requestError) {
        setProducts([])
        setCategories([])
        setError(getErrorMessage(requestError))
      } finally {
        setLoading(false)
      }
    },
    [],
  )

  useEffect(() => {
    loadBusinesses()
  }, [loadBusinesses])

  useEffect(() => {
    loadWorkspaceData(businessId)
  }, [businessId, loadWorkspaceData])

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

  function handleBusinessChange(value) {
    setBusinessId(value)
    resetFilters()
    setFormOpen(false)
    setEditingProduct(null)
  }

  function openCreateForm() {
    setEditingProduct(null)
    setFormOpen(true)
    setError('')
  }

  function openEditForm(product) {
    setEditingProduct(product)
    setFormOpen(true)
    setError('')
  }

  function closeForm() {
    if (saving) {
      return
    }

    setFormOpen(false)
    setEditingProduct(null)
  }

  async function handleSubmit(payload) {
    if (!businessId) {
      setError('Please select a business first.')
      return
    }

    try {
      setSaving(true)
      setError('')

      if (editingProduct) {
        await updateProduct(
          businessId,
          editingProduct.id,
          payload,
        )
      } else {
        await createProduct(
          businessId,
          payload,
        )
      }

      await loadWorkspaceData(businessId)

      setFormOpen(false)
      setEditingProduct(null)
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setSaving(false)
    }
  }

  if (loading && !businessId) {
    return <ProductLoading />
  }

  return (
    <main className="products-page">
      <ProductHeader
        businesses={businesses}
        businessId={businessId}
        onBusinessChange={handleBusinessChange}
        productCount={products.length}
        onAddProduct={openCreateForm}
      />

      {error && (
        <div
          className="products-error"
          role="alert"
        >
          {error}
        </div>
      )}

      {businessId && (
        <>
          <ProductStats products={products} />

          <ProductFilters
            search={search}
            catalogFilter={catalogFilter}
            catalogGroups={CATALOG_GROUPS}
            catalogCounts={catalogCounts}
            categoryFilter={categoryFilter}
            stockFilter={stockFilter}
            statusFilter={statusFilter}
            categories={filteredCategories}
            onSearchChange={setSearch}
            onCatalogChange={handleCatalogChange}
            onCategoryChange={setCategoryFilter}
            onStockChange={setStockFilter}
            onStatusChange={setStatusFilter}
            resultCount={filteredProducts.length}
            totalCount={products.length}
            onClear={resetFilters}
          />

          <ProductTable
            products={filteredProducts}
            loading={loading}
            hasFilters={hasActiveFilters}
            onClear={resetFilters}
            onEdit={openEditForm}
            onAddProduct={openCreateForm}
          />
        </>
      )}

      {formOpen && (
        <ProductForm
          categories={categories}
          product={editingProduct}
          loading={saving}
          error={error}
          onSubmit={handleSubmit}
          onClose={closeForm}
        />
      )}
    </main>
  )
}

export default Products
