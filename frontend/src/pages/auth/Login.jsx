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
} from 'react-router-dom'

import { useAuth } from '../../context/AuthContext.jsx'
import { loginUser } from '../../services/auth.js'

function Login() {
  const navigate = useNavigate()
  const { saveSession } = useAuth()

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()

    setError('')
    setLoading(true)

    try {
      const session = await loginUser(
        email,
        password,
      )

      saveSession(session, session.user)

      navigate('/dashboard', {
        replace: true,
      })
    } catch (requestError) {
      const responseData =
        requestError.response?.data

      const message =
        responseData?.detail ||
        responseData?.message ||
        responseData?.email?.[0] ||
        'Unable to sign in. Please check your credentials.'

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
          <span>Welcome back</span>

          <h1>
            Sign in to your business.
          </h1>

          <p>
            Access your inventory, sales,
            purchases, and business insights.
          </p>
        </div>

        <form onSubmit={handleSubmit}>
          <label htmlFor="email">
            Email address
          </label>

          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) =>
              setEmail(event.target.value)
            }
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
              type={
                showPassword
                  ? 'text'
                  : 'password'
              }
              value={password}
              onChange={(event) =>
                setPassword(event.target.value)
              }
              placeholder="Enter your password"
              autoComplete="current-password"
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
              ? 'Signing in...'
              : 'Sign in'}

            {!loading && (
              <ArrowRight size={17} />
            )}
          </button>
        </form>

        <p className="auth-footer">
          Need an account?{' '}
          <Link to="/">
            Contact StockPilot
          </Link>
        </p>
      </section>
    </main>
  )
}

export default Login
