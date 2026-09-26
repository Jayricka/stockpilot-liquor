import {
  ArrowRight,
  Check,
} from 'lucide-react'

const plans = [
  {
    name: 'Starter',
    price: '999',
    description:
      'For small liquor businesses ready to move beyond manual stock tracking.',
    features: [
      '1 business workspace',
      'Products and categories',
      'Inventory management',
      'POS and sales',
      'Purchases and suppliers',
      'Deliveries',
      'Dashboard',
      'Basic reports',
      '1 staff member',
    ],
    action: 'Start Free',
    href: '/register?plan=starter',
  },
  {
    name: 'Growth',
    price: '1,999',
    description:
      'For growing liquor businesses that need stronger team and operational control.',
    features: [
      'Everything in Starter',
      'Up to 5 team members',
      'Full sales and purchase reports',
      'Profit visibility',
      'Low-stock monitoring',
      'Team roles',
      'Business-level insights',
      'Delivery management',
      'Priority support',
    ],
    action: 'Start Free',
    href: '/register?plan=growth',
    popular: true,
  },
  {
    name: 'Business',
    price: '3,999',
    description:
      'For established operators with more teams and business workspaces.',
    features: [
      'Everything in Growth',
      'Multiple business workspaces',
      'Larger team capacity',
      'Advanced business reporting',
      'Expanded operational visibility',
      'Priority support',
      'Business onboarding',
      'Custom requirements discussion',
    ],
    action: 'Talk to Us',
    href: '/register?plan=business',
  },
]

function Pricing() {
  return (
    <section
      className="section pricing-section"
      id="pricing"
    >
      <div className="pricing-heading">
        <div>
          <div className="section-label">
            Pricing
          </div>

          <h2>
            Start with what your business needs.
          </h2>

          <p>
            Simple plans built around the way
            liquor businesses actually buy, stock,
            sell, deliver, and track performance.
          </p>
        </div>

        <div className="pricing-note">
          <span>Launch pricing</span>
          <strong>Monthly</strong>
          <small>
            Upgrade as your operation grows.
          </small>
        </div>
      </div>

      <div className="pricing-grid">
        {plans.map((plan) => (
          <article
            className={`pricing-plan ${
              plan.popular
                ? 'pricing-plan-featured'
                : ''
            }`}
            key={plan.name}
          >
            {plan.popular && (
              <div className="pricing-badge">
                Recommended
              </div>
            )}

            <div className="pricing-plan-header">
              <span className="pricing-plan-name">
                {plan.name}
              </span>

              <p>{plan.description}</p>

              <div className="pricing-price">
                <span>KES</span>
                <strong>{plan.price}</strong>
                <small>/month</small>
              </div>
            </div>

            <div className="pricing-divider" />

            <ul className="pricing-features">
              {plan.features.map((feature) => (
                <li key={feature}>
                  <Check size={15} />
                  <span>{feature}</span>
                </li>
              ))}
            </ul>

            <a
              className={`button ${
                plan.popular
                  ? 'button-primary'
                  : 'button-secondary'
              } pricing-action`}
              href={plan.href}
            >
              {plan.action}
              <ArrowRight size={16} />
            </a>
          </article>
        ))}
      </div>

      <div className="pricing-footer">
        <div>
          <strong>
            One system for the full stock cycle.
          </strong>

          <p>
            Buy stock, receive it, sell it, track
            what remains, and understand how the
            business is performing.
          </p>
        </div>

        <a
          className="pricing-demo-link"
          href="/demo"
        >
          See how StockPilot works
          <ArrowRight size={15} />
        </a>
      </div>
    </section>
  )
}

export default Pricing
