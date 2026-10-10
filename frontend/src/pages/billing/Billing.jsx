import BillingHeader from '../../components/billing/BillingHeader'
import PaymentForm from '../../components/billing/PaymentForm'
import PlanCard from '../../components/billing/PlanCard'
import SubscriptionCard from '../../components/billing/SubscriptionCard'

import { usePayment } from './hooks/usePayment'
import { useBillingWorkspace } from './hooks/useBillingWorkspace'

function Billing() {
  const workspace = useBillingWorkspace()
  const payment = usePayment()

  if (workspace.loading) {
    return (
      <section className="billing-page">
        <BillingHeader />

        <div
          className="billing-state"
          role="status"
        >
          <h2>Loading billing...</h2>

          <p>
            Preparing your subscription and
            available plans.
          </p>
        </div>
      </section>
    )
  }

  const subscription = workspace.subscription
  const currentPlan = subscription?.plan

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
        subscription={subscription}
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

        {workspace.plans.length > 0 ? (
          <div className="billing-plan-grid">
            {workspace.plans.map((plan) => (
              <PlanCard
                key={plan.code}
                plan={plan}
                currentPlanCode={currentPlan?.code}
              />
            ))}
          </div>
        ) : (
          <div className="billing-state">
            <h2>No plans available</h2>

            <p>
              Billing plans could not be loaded.
              Please try again later.
            </p>
          </div>
        )}
      </section>

      <PaymentForm
        defaultAmount={currentPlan?.price}
        currency={currentPlan?.currency || 'KES'}
        loading={payment.loading}
        error={payment.error}
        payment={payment.payment}
        onSubmit={payment.initiatePayment}
      />
    </section>
  )
}

export default Billing
