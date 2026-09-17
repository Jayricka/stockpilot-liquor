import { Bell } from 'lucide-react'

import { useAuth } from '../../context/AuthContext.jsx'

function Topbar() {
  const { user } = useAuth()

  const username = user?.username || 'Business owner'

  return (
    <header className="app-topbar">
      <div>
        <span className="topbar-label">
          Business workspace
        </span>

        <h1>StockPilot</h1>
      </div>

      <div className="topbar-actions">
        <button
          className="notification-button"
          type="button"
          aria-label="Notifications"
        >
          <Bell size={18} />
          <span />
        </button>

        <div className="user-menu">
          <div className="user-avatar">
            {username.charAt(0).toUpperCase()}
          </div>

          <div>
            <strong>{username}</strong>
            <small>Business user</small>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Topbar
