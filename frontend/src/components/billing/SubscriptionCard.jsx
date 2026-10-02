function formatDate(value) {
  if (!value) {
    return '—'
  }

  return new Date(value).toLocaleDateString()
}

function SubscriptionCard({
  subscription,
  isTrialing,
  trialDaysRemaining,
}) {
  if (!subscription) {
    return (
      <section className="billing-card">
        <h2>Subscription</h2>

        <p>
          No subscription is currently available
          for this business.
        </p>
      </section>
    )
  }

  const plan = subscription.plan

  return (
    <section className="billing-card">
      <div className="billing-card-header">
        <div>
          <p className="billing-label">
            Current plan
          </p>

          <h2>
            {plan?.name || 'Unknown plan'}
          </h2>
        </div>

        <span className="billing-status">
          {subscription.status}
        </span>
      </div>

      {isTrialing && (
        <div className="billing-trial">
          <strong>
            {trialDaysRemaining} days remaining
          </strong>

          <span>
            Your trial ends on{' '}
            {formatDate(
              subscription.trial_ends_at,
            )}
          </span>
        </div>
      )}

      <div className="billing-details">
        <div>
          <span>Status</span>
          <strong>
            {subscription.status}
          </strong>
        </div>

        <div>
          <span>Plan price</span>
          <strong>
            {plan?.currency || 'KES'}{' '}
            {plan?.price ?? '—'}
          </strong>
        </div>

        <div>
          <span>Trial</span>
          <strong>
            {plan?.trial_days ?? 0} days
          </strong>
        </div>

        <div>
          <span>Current period</span>
          <strong>
            {formatDate(
              subscription.current_period_start,
            )}
            {' — '}
            {formatDate(
              subscription.current_period_end,
            )}
          </strong>
        </div>
      </div>
    </section>
  )
}

export default SubscriptionCard
