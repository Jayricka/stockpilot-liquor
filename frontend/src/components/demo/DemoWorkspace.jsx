import {
  CheckCircle2,
  Loader2,
  Package,
  RefreshCw,
  ShoppingCart,
  ShieldCheck,
  TrendingUp,
  X,
} from 'lucide-react'

import {
  useCallback,
  useEffect,
  useState,
} from 'react'

import { useNavigate } from 'react-router-dom'

import {
  getDemoState,
  makeDemoSale,
  receiveDemoStock,
} from '../../services/demo'

import DemoActionCard from './DemoActionCard'
import DemoMetric from './DemoMetric'
import DemoProducts from './DemoProducts'
import DemoSidebar from './DemoSidebar'
import DemoWorkspaceHeader from './DemoWorkspaceHeader'

function DemoWorkspace({ token }) {
  const navigate = useNavigate()

  const [state, setState] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [actionError, setActionError] =
    useState('')
  const [message, setMessage] = useState('')
  const [actionLoading, setActionLoading] =
    useState(false)
  const [actionType, setActionType] = useState('')
  const [selectedProduct, setSelectedProduct] =
    useState('')
  const [quantity, setQuantity] = useState('1')

  const products = state?.products || []

  useEffect(() => {
    let cancelled = false

    async function fetchDemo() {
      try {
        const data = await getDemoState(token)

        if (cancelled) {
          return
        }

        setState(data)
        setError('')

        setSelectedProduct((current) =>
          current ||
          String(
            data.products?.[0]?.id || '',
          ),
        )
      } catch (err) {
        if (cancelled) {
          return
        }

        setError(
          err.response?.data?.detail ||
            'This demo session is unavailable or has expired.',
        )
      } finally {
        if (!cancelled) {
          setLoading(false)
        }
      }
    }

    fetchDemo()

    return () => {
      cancelled = true
    }
  }, [token])

  const loadDemo = useCallback(async () => {
    try {
      setLoading(true)
      setError('')

      const data = await getDemoState(token)

      setState(data)

      setSelectedProduct((current) =>
        current ||
        String(
          data.products?.[0]?.id || '',
        ),
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'This demo session is unavailable or has expired.',
      )
    } finally {
      setLoading(false)
    }
  }, [token])

  const totalStock = products.reduce(
    (sum, product) =>
      sum +
      Number(product.stock_quantity || 0),
    0,
  )

  const lowStock = products.filter(
    (product) =>
      Number(product.stock_quantity || 0) <=
      Number(product.reorder_level || 0),
  ).length

  async function handleAction(type) {
    const parsedQuantity = Number(quantity)

    if (
      !selectedProduct ||
      !Number.isFinite(parsedQuantity) ||
      parsedQuantity <= 0
    ) {
      setActionError(
        'Select a product and enter a valid quantity.',
      )
      return
    }

    try {
      setActionLoading(true)
      setActionType(type)
      setActionError('')
      setMessage('')

      const result =
        type === 'purchase'
          ? await receiveDemoStock(
              token,
              selectedProduct,
              parsedQuantity,
            )
          : await makeDemoSale(
              token,
              selectedProduct,
              parsedQuantity,
            )

      setMessage(result.message)

      await loadDemo()
    } catch (err) {
      setActionError(
        err.response?.data?.detail ||
          'The demo action could not be completed.',
      )
    } finally {
      setActionLoading(false)
      setActionType('')
    }
  }

  if (loading) {
    return <DemoLoading />
  }

  if (error || !state) {
    return (
      <DemoError
        message={error}
        onRestart={() => navigate('/demo')}
      />
    )
  }

  return (
    <main className="demo-workspace-page">
      <DemoWorkspaceHeader />

      <div className="demo-workspace-shell">
        <DemoSidebar
          businessName={state.business.name}
        />

        <section className="demo-workspace-content">
          <DemoHeading
            businessName={state.business.name}
            onRefresh={loadDemo}
          />

          <div className="demo-summary-grid">
            <DemoMetric
              icon={<Package size={18} />}
              label="Products"
              value={products.length}
            />

            <DemoMetric
              icon={<TrendingUp size={18} />}
              label="Units in stock"
              value={totalStock}
            />

            <DemoMetric
              icon={
                <ShieldCheck size={18} />
              }
              label="Low stock"
              value={lowStock}
            />
          </div>

          <div className="demo-actions-grid">
            <DemoActionCard
              title="Receive stock"
              description="Add inventory through the purchase workflow."
              icon={<Package size={19} />}
              products={products}
              selectedProduct={
                selectedProduct
              }
              quantity={quantity}
              onProductChange={
                setSelectedProduct
              }
              onQuantityChange={setQuantity}
              onSubmit={() =>
                handleAction('purchase')
              }
              loading={
                actionLoading &&
                actionType === 'purchase'
              }
              buttonLabel="Receive stock"
            />

            <DemoActionCard
              title="Make a sale"
              description="Complete a sale and watch inventory decrease."
              icon={
                <ShoppingCart size={19} />
              }
              products={products}
              selectedProduct={
                selectedProduct
              }
              quantity={quantity}
              onProductChange={
                setSelectedProduct
              }
              onQuantityChange={setQuantity}
              onSubmit={() =>
                handleAction('sale')
              }
              loading={
                actionLoading &&
                actionType === 'sale'
              }
              buttonLabel="Complete sale"
            />
          </div>

          {(message || actionError) && (
            <div
              className={
                actionError
                  ? 'demo-action-message is-error'
                  : 'demo-action-message'
              }
              role="status"
            >
              {actionError ? (
                <X size={17} />
              ) : (
                <CheckCircle2 size={17} />
              )}

              <span>
                {actionError || message}
              </span>
            </div>
          )}

          <DemoProducts
            products={products}
          />
        </section>
      </div>
    </main>
  )
}

function DemoHeading({
  businessName,
  onRefresh,
}) {
  return (
    <div className="demo-page-heading">
      <div>
        <span className="demo-eyebrow">
          Demo workspace
        </span>

        <h1>{businessName}</h1>

        <p>
          Try the core StockPilot workflow
          using real inventory operations.
        </p>
      </div>

      <button
        className="demo-refresh-button"
        type="button"
        onClick={onRefresh}
      >
        <RefreshCw size={16} />
        Refresh
      </button>
    </div>
  )
}

function DemoLoading() {
  return (
    <main className="demo-workspace-page">
      <div className="demo-workspace-loading">
        <Loader2
          size={28}
          className="demo-spin"
        />

        <span>
          Loading your demo workspace...
        </span>
      </div>
    </main>
  )
}

function DemoError({
  message,
  onRestart,
}) {
  return (
    <main className="demo-workspace-page">
      <div className="demo-workspace-error">
        <div className="demo-error-icon">
          <X size={20} />
        </div>

        <span className="demo-eyebrow">
          Demo unavailable
        </span>

        <h1>
          This demo session is no longer
          available.
        </h1>

        <p>
          {message ||
            'Start a new demo workspace to continue exploring StockPilot.'}
        </p>

        <button
          className="button button-primary"
          type="button"
          onClick={onRestart}
        >
          Start new demo
        </button>
      </div>
    </main>
  )
}

export default DemoWorkspace
