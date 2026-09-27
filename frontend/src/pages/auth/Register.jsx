import {
  ArrowRight,
  Eye,
  EyeOff,
  Zap,
} from 'lucide-react'
import {
  Link,
  useSearchParams,
} from 'react-router-dom'

import { useRegisterForm } from './hooks/useRegisterForm'

function Register() {
  const [searchParams] = useSearchParams()
  const requestedPlan = searchParams.get('plan')

  const {
    selectedPlan,
    formData,
    confirmPassword,
    showPassword,
    showConfirmPassword,
    error,
    loading,
    handleChange,
    handleSubmit,
    setConfirmPassword,
    setShowPassword,
    setShowConfirmPassword,
  } = useRegisterForm(requestedPlan)

  const planName =
    selectedPlan.charAt(0).toUpperCase() +
    selectedPlan.slice(1)

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

          <strong>{planName}</strong>

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
