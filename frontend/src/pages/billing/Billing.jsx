import BillingHeader from '../../components/billing/BillingHeader'
import PlanCard from '../../components/billing/PlanCard'
import SubscriptionCard from '../../components/billing/SubscriptionCard'

import { useBillingWorkspace } from './hooks/useBillingWorkspace'

function Billing() {
  const workspace =
    useBillingWorkspace()

  if (workspace.loading) {
    return (
      <section className="billing-page">
        <BillingHeader />

        <div className="billing-state">
          <h2>Loading billing...</h2>

          <p>
            Preparing your subscription and
            available plans.
          </p>
        </div>
      </section>
    )
  }

  return (
    <section className="billing-page">
      <BillingHeader />

      {workspace.error && (
        <div
          className="billing-error"
          role="alert"
        >
          {workspace.error}
        </div>
      )}

      <SubscriptionCard
        subscription={workspace.subscription}
        isTrialing={workspace.isTrialing}
        trialDaysRemaining={
          workspace.trialDaysRemaining
        }
      />

      <section className="billing-plans">
        <div className="billing-section-header">
          <div>
            <p className="billing-label">
              Available plans
            </p>

            <h2>Choose a plan</h2>
          </div>
        </div>

        <div className="billing-plan-grid">
          {workspace.plans.map((plan) => (
            <PlanCard
              key={plan.code}
              plan={plan}
              currentPlanCode={
                workspace.subscription?.plan?.code
              }
            />
          ))}
        </div>
      </section>
    </section>
  )
}

export default Billing
