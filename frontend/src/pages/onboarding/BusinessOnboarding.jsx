import {
  ArrowRight,
  Building2,
  Check,
  Zap,
} from 'lucide-react'
import { useState } from 'react'
import {
  Link,
  Navigate,
  useNavigate,
  useSearchParams,
} from 'react-router-dom'

import { useAuth } from '../../context/AuthContext.jsx'
import { onboardBusiness } from '../../services/businesses.js'

const plans = [
  {
    code: 'starter',
    name: 'Starter',
    price: '999',
  },
  {
    code: 'growth',
    name: 'Growth',
    price: '1,999',
  },
  {
    code: 'business',
    name: 'Business',
    price: '3,999',
  },
]

function BusinessOnboarding() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { isAuthenticated } = useAuth()

  const requestedPlan = searchParams.get('plan')

  const initialPlan = plans.some(
    (plan) => plan.code === requestedPlan,
  )
    ? requestedPlan
    : 'starter'

  const [formData, setFormData] = useState({
    name: '',
    business_type: 'liquor_store',
    phone: '',
    email: '',
    address: '',
    license_number: '',
    plan: initialPlan,
  })

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login"
        replace
      />
    )
  }

  function handleChange(event) {
    const { name, value } = event.target

    setFormData((current) => ({
      ...current,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()

    setError('')
    setLoading(true)

    try {
      const response = await onboardBusiness(
        formData,
      )

      sessionStorage.setItem(
        'stockpilot-business',
        JSON.stringify(response.business),
      )

      sessionStorage.setItem(
        'stockpilot-subscription',
        JSON.stringify(response.subscription),
      )

      navigate('/dashboard', {
        replace: true,
      })
    } catch (requestError) {
      const responseData =
        requestError.response?.data

      const message =
        responseData?.detail ||
        responseData?.name?.[0] ||
        responseData?.phone?.[0] ||
        responseData?.plan?.[0] ||
        'Unable to create your business. Please try again.'

      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="onboarding-page">
      <section className="onboarding-card">
        <Link
          className="auth-brand"
          to="/"
        >
          <span className="brand-mark">
            <Zap
              size={18}
              strokeWidth={2.5}
            />
          </span>

          <span>
            <strong>StockPilot</strong>
            <small>
              Liquor business management
            </small>
          </span>
        </Link>

        <div className="onboarding-heading">
          <span>
            <Building2 size={15} />
            Business setup
          </span>

          <h1>
            Tell us about your business.
          </h1>

          <p>
            Set up your workspace and start your
            7-day free trial.
          </p>
        </div>

        <div className="trial-notice">
          <div>
            <strong>
              Your 7-day trial starts now
            </strong>

            <span>
              No payment required. You'll have full
              access during the trial.
            </span>
          </div>

          <Check size={20} />
        </div>

        <form onSubmit={handleSubmit}>
          <div className="onboarding-section">
            <div className="onboarding-section-heading">
              <strong>Business details</strong>
              <span>
                Required information
              </span>
            </div>

            <label htmlFor="business-name">
              Business name
            </label>

            <input
              id="business-name"
              name="name"
              type="text"
              value={formData.name}
              onChange={handleChange}
              placeholder="e.g. Westlands Liquor Store"
              required
            />

            <div className="onboarding-form-row">
              <div>
                <label htmlFor="business-phone">
                  Business phone
                </label>

                <input
                  id="business-phone"
                  name="phone"
                  type="tel"
                  value={formData.phone}
                  onChange={handleChange}
                  placeholder="0712345678"
                  required
                />
              </div>

              <div>
                <label htmlFor="business-email">
                  Business email
                </label>

                <input
                  id="business-email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Optional"
                />
              </div>
            </div>

            <label htmlFor="business-address">
              Business address
            </label>

            <textarea
              id="business-address"
              name="address"
              value={formData.address}
              onChange={handleChange}
              placeholder="Business location or address"
              rows="3"
            />

            <label htmlFor="license-number">
              Liquor license number
            </label>

            <input
              id="license-number"
              name="license_number"
              type="text"
              value={formData.license_number}
              onChange={handleChange}
              placeholder="Optional"
            />
          </div>

          <div className="onboarding-section">
            <div className="onboarding-section-heading">
              <strong>Choose your plan</strong>
              <span>
                You can upgrade later
              </span>
            </div>

            <div className="onboarding-plans">
              {plans.map((plan) => (
                <label
                  className={`onboarding-plan ${
                    formData.plan === plan.code
                      ? 'is-selected'
                      : ''
                  }`}
                  key={plan.code}
                >
                  <input
                    type="radio"
                    name="plan"
                    value={plan.code}
                    checked={
                      formData.plan ===
                      plan.code
                    }
                    onChange={handleChange}
                  />

                  <span className="onboarding-plan-content">
                    <strong>
                      {plan.name}
                    </strong>

                    <small>
                      KES {plan.price}/month
                    </small>
                  </span>

                  {formData.plan ===
                    plan.code && (
                    <Check size={17} />
                  )}
                </label>
              ))}
            </div>
          </div>

          {error && (
            <div className="auth-error">
              {error}
            </div>
          )}

          <button
            className="auth-submit"
            type="submit"
            disabled={loading}
          >
            {loading
              ? 'Setting up workspace...'
              : 'Create business & start trial'}

            {!loading && (
              <ArrowRight size={17} />
            )}
          </button>
        </form>

        <p className="auth-footer">
          You can change your plan later from
          billing.
        </p>
      </section>
    </main>
  )
}

export default BusinessOnboarding
