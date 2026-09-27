
import ProductFilters from '../../components/products/ProductFilters'
import CategoryForm from '../../components/products/category/CategoryForm'
import ProductForm from '../../components/products/ProductForm'
import ProductHeader from '../../components/products/ProductHeader'
import ProductLoading from '../../components/products/ProductLoading'
import ProductStats from '../../components/products/ProductStats'
import ProductTable from '../../components/products/ProductTable'

import { useProductWorkspace } from './hooks/useProductWorkspace'
import { useProductFilters } from './hooks/useProductFilters'
import { useProductForm } from './hooks/useProductForm'
import { useCategoryForm } from './hooks/useCategoryForm'

function Products() {
  const workspace = useProductWorkspace()

  const filters = useProductFilters(
    workspace.products,
    workspace.categories,
  )

  const form = useProductForm({
    businessId: workspace.businessId,
    loadWorkspaceData: workspace.loadWorkspaceData,
    setError: workspace.setError,
  })

  const categoryForm = useCategoryForm({
    businessId: workspace.businessId,
    loadWorkspaceData: workspace.loadWorkspaceData,
    setError: workspace.setError,
  })

  function handleBusinessChange(value) {
    workspace.handleBusinessChange(
      value,
      filters.resetFilters,
    )
    form.closeForm()
  }

  if (
    workspace.businessLoading ||
    (workspace.loading && !workspace.businessId)
  ) {
    return <ProductLoading />
  }

  return (
    <main className="products-page">
      <ProductHeader
        businesses={workspace.businesses}
        businessId={workspace.businessId}
        onBusinessChange={handleBusinessChange}
        productCount={workspace.products.length}
        onAddProduct={form.openCreateForm}
      />

      {workspace.error && (
        <div
          className="products-error"
          role="alert"
        >
          {workspace.error}
        </div>
      )}

      {workspace.businessId && (
        <>
          <ProductStats
            products={workspace.products}
          />

          <ProductFilters
            search={filters.search}
            catalogFilter={filters.catalogFilter}
            catalogGroups={filters.catalogGroups}
            catalogCounts={filters.catalogCounts}
            categoryFilter={filters.categoryFilter}
            stockFilter={filters.stockFilter}
            statusFilter={filters.statusFilter}
            categories={filters.filteredCategories}
            onSearchChange={filters.setSearch}
            onCatalogChange={
              filters.handleCatalogChange
            }
            onCategoryChange={
              filters.setCategoryFilter
            }
            onStockChange={filters.setStockFilter}
            onStatusChange={filters.setStatusFilter}
            resultCount={
              filters.filteredProducts.length
            }
            totalCount={
              workspace.products.length
            }
            onClear={filters.resetFilters}
          />

          <ProductTable
            products={filters.filteredProducts}
            loading={workspace.loading}
            hasFilters={filters.hasActiveFilters}
            onClear={filters.resetFilters}
            onEdit={form.openEditForm}
            onAddProduct={form.openCreateForm}
          />
        </>
      )}

      {categoryForm.formOpen && (
        <CategoryForm
          loading={categoryForm.saving}
          error={workspace.error}
          onSubmit={categoryForm.handleSubmit}
          onClose={categoryForm.closeForm}
        />
      )}

      {form.formOpen && (
        <ProductForm
          categories={workspace.categories}
          product={form.editingProduct}
          loading={form.saving}
          error={workspace.error}
          onSubmit={form.handleSubmit}
          onClose={form.closeForm}
        />
      )}
    </main>
  )
}

export default Products
