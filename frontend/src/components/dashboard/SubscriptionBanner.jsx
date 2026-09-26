import {
  AlertCircle,
  CheckCircle2,
  Clock3,
} from 'lucide-react'

import { useBusiness } from '../../context/BusinessContext.jsx'

function SubscriptionBanner() {
  const {
    subscription,
    plan,
    isTrialing,
    trialDaysRemaining,
  } = useBusiness()

  if (!subscription) {
    return null
  }

  if (isTrialing) {
    return (
      <div className="subscription-banner subscription-banner-trial">
        <div className="subscription-banner-icon">
          <Clock3 size={18} />
        </div>

        <div className="subscription-banner-content">
          <strong>
            {plan?.name || 'StockPilot'} free trial
          </strong>

          <span>
            {trialDaysRemaining}{' '}
            {trialDaysRemaining === 1
              ? 'day'
              : 'days'}{' '}
            remaining. You have full access to
            StockPilot during your trial.
          </span>
        </div>
      </div>
    )
  }

  if (subscription.status === 'ACTIVE') {
    return (
      <div className="subscription-banner subscription-banner-active">
        <div className="subscription-banner-icon">
          <CheckCircle2 size={18} />
        </div>

        <div className="subscription-banner-content">
          <strong>
            {plan?.name || 'StockPilot'} subscription active
          </strong>

          <span>
            Your StockPilot subscription is active and
            your workspace is fully operational.
          </span>
        </div>
      </div>
    )
  }

  return (
    <div className="subscription-banner subscription-banner-warning">
      <div className="subscription-banner-icon">
        <AlertCircle size={18} />
      </div>

      <div className="subscription-banner-content">
        <strong>
          Subscription action required
        </strong>

        <span>
          Your subscription is currently{' '}
          {subscription.status?.toLowerCase() ||
            'inactive'}
          . Upgrade your plan to continue using
          operational features.
        </span>
      </div>

      <button
        className="subscription-banner-action"
        type="button"
      >
        View plans
      </button>
    </div>
  )
}

export default SubscriptionBanner
