import {
  ArrowRight,
  Loader2,
  Play,
  ShieldCheck,
  Zap,
} from 'lucide-react'

import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import { startDemo } from '../../services/demo'

function DemoStart() {
  const navigate = useNavigate()

  const [starting, setStarting] =
    useState(false)

  const [error, setError] =
    useState('')

  async function handleStartDemo() {
    try {
      setStarting(true)
      setError('')

      const session =
        await startDemo()

      navigate(`/demo/${session.token}`)
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to start the demo. Please try again.',
      )
    } finally {
      setStarting(false)
    }
  }

  return (
    <main className="demo-start-page">
      <div className="demo-start-shell">
        <div className="demo-start-brand">
          <span className="brand-mark">
            <Zap
              size={18}
              strokeWidth={2.5}
            />
          </span>

          <span>
            StockPilot
          </span>
        </div>

        <div className="demo-start-content">
          <div className="demo-eyebrow">
            <Play size={15} />
            Interactive demo
          </div>

          <h1>
            See StockPilot in action.
          </h1>

          <p>
            Explore a working liquor business
            workspace without creating an account.
            Receive stock, make a sale, and watch
            your inventory update in real time.
          </p>

          <button
            className="button button-primary demo-start-button"
            type="button"
            onClick={handleStartDemo}
            disabled={starting}
          >
            {starting
              ? 'Preparing demo...'
              : 'Start free demo'}

            {starting ? (
              <Loader2
                size={17}
                className="demo-spin"
              />
            ) : (
              <ArrowRight size={17} />
            )}
          </button>

          {error && (
            <div
              className="demo-error"
              role="alert"
            >
              {error}
            </div>
          )}

          <div className="demo-trust">
            <ShieldCheck size={17} />

            <span>
              No signup. No payment. Demo data is
              isolated from real businesses.
            </span>
          </div>
        </div>

        <DemoPreview />
      </div>
    </main>
  )
}

function DemoPreview() {
  return (
    <div className="demo-start-preview">
      <div className="demo-preview-top">
        <span />
        <span />
        <span />
      </div>

      <div className="demo-preview-body">
        <aside>
          <strong>StockPilot</strong>

          <span className="active">
            Overview
          </span>

          <span>Products</span>
          <span>Sales</span>
          <span>Purchases</span>
          <span>Reports</span>
        </aside>

        <div className="demo-preview-main">
          <small>Demo workspace</small>

          <h2>
            Nairobi Liquor Store
          </h2>

          <div className="demo-preview-metrics">
            <div>
              <span>Inventory</span>
              <strong>Live</strong>
            </div>

            <div>
              <span>Products</span>
              <strong>4</strong>
            </div>

            <div>
              <span>Stock control</span>
              <strong>Live</strong>
            </div>
          </div>

          <div className="demo-preview-table">
            <span>Product</span>
            <span>Stock</span>
            <span>Status</span>

            <span>
              Jameson 750ml
            </span>

            <strong>18</strong>

            <em>Healthy</em>

            <span>
              Gordon's Gin
            </span>

            <strong>12</strong>

            <em>Healthy</em>

            <span>
              Four Cousins
            </span>

            <strong>8</strong>

            <em>Monitor</em>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DemoStart
