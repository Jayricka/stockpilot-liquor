import { Bell } from 'lucide-react'

import { useAuth } from '../../context/AuthContext.jsx'
import { useBusiness } from '../../context/BusinessContext.jsx'

function Topbar() {
  const { user } = useAuth()
  const {
    business,
    subscription,
    plan,
    isTrialing,
    trialDaysRemaining,
  } = useBusiness()

  const displayName =
    user?.full_name ||
    user?.first_name ||
    user?.email ||
    'Business owner'

  const businessName =
    business?.name || 'Business workspace'

  const subscriptionLabel =
    isTrialing
      ? `${plan?.name || 'Plan'} · Trial`
      : subscription?.status === 'ACTIVE'
        ? `${plan?.name || 'Plan'} · Active`
        : 'Subscription inactive'

  return (
    <header className="app-topbar">
      <div>
        <span className="topbar-label">
          {businessName}
        </span>

        <h1>StockPilot</h1>
      </div>

      <div className="topbar-actions">
        <div className="topbar-subscription">
          <strong>
            {subscriptionLabel}
          </strong>

          {isTrialing && (
            <span>
              {trialDaysRemaining}{' '}
              {trialDaysRemaining === 1
                ? 'day'
                : 'days'}{' '}
              remaining
            </span>
          )}
        </div>

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
            {displayName
              .charAt(0)
              .toUpperCase()}
          </div>

          <div>
            <strong>{displayName}</strong>
            <small>Business owner</small>
          </div>
        </div>
      </div>
    </header>
  )
}

export default Topbar
