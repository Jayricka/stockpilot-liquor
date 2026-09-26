import {
  ArrowRight,
  Eye,
  EyeOff,
  Zap,
} from 'lucide-react'
import { useState } from 'react'
import {
  Link,
  useNavigate,
  useSearchParams,
} from 'react-router-dom'

import { useAuth } from '../../context/AuthContext.jsx'
import { registerUser } from '../../services/auth.js'

const validPlans = [
  'starter',
  'growth',
  'business',
]

function Register() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { saveSession } = useAuth()

  const requestedPlan = searchParams.get('plan')

  const selectedPlan = validPlans.includes(
    requestedPlan,
  )
    ? requestedPlan
    : 'starter'

  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
  })

  const [confirmPassword, setConfirmPassword] =
    useState('')

  const [showPassword, setShowPassword] =
    useState(false)

  const [showConfirmPassword, setShowConfirmPassword] =
    useState(false)

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

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

    if (formData.password !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    if (formData.password.length < 8) {
      setError(
        'Password must be at least 8 characters.',
      )
      return
    }

    setLoading(true)

    try {
      const session = await registerUser(formData)

      saveSession(session, session.user)

      navigate(
        `/onboarding?plan=${selectedPlan}`,
        { replace: true },
      )
    } catch (requestError) {
      const responseData =
        requestError.response?.data

      const message =
        responseData?.detail ||
        responseData?.email?.[0] ||
        responseData?.password?.[0] ||
        'Unable to create your account. Please try again.'

      setError(message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
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

        <div className="auth-heading">
          <span>Get started</span>

          <h1>
            Create your StockPilot account.
          </h1>

          <p>
            Start your 7-day free trial with no
            payment required.
          </p>
        </div>

        <div className="auth-plan-summary">
          <span>Selected plan</span>

          <strong>
            {selectedPlan.charAt(0).toUpperCase() +
              selectedPlan.slice(1)}
          </strong>

          <small>
            7-day free trial
          </small>
        </div>

        <form onSubmit={handleSubmit}>
          <div className="auth-form-row">
            <div>
              <label htmlFor="first_name">
                First name
              </label>

              <input
                id="first_name"
                name="first_name"
                type="text"
                value={formData.first_name}
                onChange={handleChange}
                placeholder="First name"
                autoComplete="given-name"
                required
              />
            </div>

            <div>
              <label htmlFor="last_name">
                Last name
              </label>

              <input
                id="last_name"
                name="last_name"
                type="text"
                value={formData.last_name}
                onChange={handleChange}
                placeholder="Last name"
                autoComplete="family-name"
                required
              />
            </div>
          </div>

          <label htmlFor="email">
            Email address
          </label>

          <input
            id="email"
            name="email"
            type="email"
            value={formData.email}
            onChange={handleChange}
            placeholder="you@example.com"
            autoComplete="email"
            required
          />

          <label htmlFor="password">
            Password
          </label>

          <div className="password-field">
            <input
              id="password"
              name="password"
              type={
                showPassword
                  ? 'text'
                  : 'password'
              }
              value={formData.password}
              onChange={handleChange}
              placeholder="At least 8 characters"
              autoComplete="new-password"
              required
            />

            <button
              type="button"
              onClick={() =>
                setShowPassword(
                  (visible) => !visible,
                )
              }
              aria-label={
                showPassword
                  ? 'Hide password'
                  : 'Show password'
              }
            >
              {showPassword ? (
                <EyeOff size={18} />
              ) : (
                <Eye size={18} />
              )}
            </button>
          </div>

          <label htmlFor="confirm_password">
            Confirm password
          </label>

          <div className="password-field">
            <input
              id="confirm_password"
              type={
                showConfirmPassword
                  ? 'text'
                  : 'password'
              }
              value={confirmPassword}
              onChange={(event) =>
                setConfirmPassword(
                  event.target.value,
                )
              }
              placeholder="Repeat your password"
              autoComplete="new-password"
              required
            />

            <button
              type="button"
              onClick={() =>
                setShowConfirmPassword(
                  (visible) => !visible,
                )
              }
              aria-label={
                showConfirmPassword
                  ? 'Hide password'
                  : 'Show password'
              }
            >
              {showConfirmPassword ? (
                <EyeOff size={18} />
              ) : (
                <Eye size={18} />
              )}
            </button>
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
              ? 'Creating account...'
              : 'Continue'}

            {!loading && (
              <ArrowRight size={17} />
            )}
          </button>
        </form>

        <p className="auth-footer">
          Already have an account?{' '}
          <Link to="/login">
            Sign in
          </Link>
        </p>
      </section>
    </main>
  )
}

export default Register
