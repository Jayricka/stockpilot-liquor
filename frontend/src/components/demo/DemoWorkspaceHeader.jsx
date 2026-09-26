import { Zap } from 'lucide-react'
import { useNavigate } from 'react-router-dom'

function DemoWorkspaceHeader() {
  const navigate = useNavigate()

  return (
    <header className="demo-workspace-topbar">
      <div className="demo-workspace-brand">
        <span className="brand-mark">
          <Zap
            size={18}
            strokeWidth={2.5}
          />
        </span>

        <div>
          <strong>StockPilot</strong>
          <span>
            Interactive workspace
          </span>
        </div>
      </div>

      <div className="demo-mode">
        <span />
        DEMO MODE
      </div>

      <button
        className="demo-exit-button"
        type="button"
        onClick={() => navigate('/')}
      >
        Exit demo
      </button>
    </header>
  )
}

export default DemoWorkspaceHeader
