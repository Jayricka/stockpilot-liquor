function PlanCard({
  plan,
  currentPlanCode,
}) {
  const isCurrent =
    plan.code === currentPlanCode

  return (
    <article
      className={`billing-plan-card${
        isCurrent
          ? ' billing-plan-card-current'
          : ''
      }`}
    >
      <div className="billing-plan-header">
        <div>
          <p className="billing-label">
            Plan
          </p>

          <h3>{plan.name}</h3>
        </div>

        {isCurrent && (
          <span className="billing-plan-badge">
            Current
          </span>
        )}
      </div>

      <div className="billing-plan-price">
        <strong>
          {plan.currency} {plan.price}
        </strong>

        <span>per billing period</span>
      </div>

      <p className="billing-plan-trial">
        {plan.trial_days}-day trial
      </p>

      <button
        type="button"
        disabled={isCurrent}
        className="billing-plan-action"
      >
        {isCurrent
          ? 'Current plan'
          : 'Choose plan'}
      </button>
    </article>
  )
}

export default PlanCard
