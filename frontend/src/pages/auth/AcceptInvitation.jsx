
import {
  ArrowRight,
  CheckCircle2,
  Zap,
} from 'lucide-react'
import { useState } from 'react'
import {
  Link,
  useNavigate,
  useSearchParams,
} from 'react-router-dom'

import { useAuth } from '../../context/AuthContext.jsx'
import { useBusiness } from '../../context/BusinessContext.jsx'
import { acceptBusinessInvitation } from '../../services/settings.js'
import { getSafeNextPath } from '../../utils/navigation.js'

function AcceptInvitation() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()

  const { isAuthenticated } = useAuth()
  const { refreshBusinesses } = useBusiness()

  const token = searchParams.get('token') || ''

  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const acceptancePath = token
    ? `/invitations/accept?token=${encodeURIComponent(token)}`
    : '/invitations/accept'

  const nextPath = getSafeNextPath(acceptancePath)

  async function handleAccept() {
    if (!token || !isAuthenticated || loading) {
      return
    }

    let invitationAccepted = false

    try {
      setLoading(true)
      setError('')

      await acceptBusinessInvitation(token)

      invitationAccepted = true

      await refreshBusinesses()

      navigate('/dashboard', {
        replace: true,
      })
    } catch (requestError) {
      if (invitationAccepted) {
        setError(
          'Your invitation was accepted, but your workspace could not be refreshed. Reload the page to load your updated access.',
        )

        return
      }

      const data = requestError.response?.data

      const message =
        data?.detail ||
        data?.token?.[0] ||
        'Unable to accept this invitation. It may have expired, been revoked, or been accepted already.'

      setError(
        typeof message === 'string'
          ? message
          : 'Unable to accept this invitation.',
      )
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-card">
        <Link className="auth-brand" to="/">
          <span className="brand-mark">
            <Zap size={18} strokeWidth={2.5} />
          </span>

          <span>
            <strong>StockSafi</strong>
            <small>Liquor business management</small>
          </span>
        </Link>

        <div className="auth-heading">
          <span>Team invitation</span>

          <h1>Join your team.</h1>

          <p>
            Accept your invitation to access an existing
            business workspace on StockSafi.
          </p>
        </div>

        {!token ? (
          <div className="auth-error" role="alert">
            This invitation link is missing its token.
            Ask the person who invited you for a new link.
          </div>
        ) : isAuthenticated ? (
          <>
            <p>
              Continue with your signed-in account. Its
              email address must match the invited email.
            </p>

            {error && (
              <div className="auth-error" role="alert">
                {error}
              </div>
            )}

            <button
              className="auth-submit"
              type="button"
              onClick={handleAccept}
              disabled={loading}
            >
              {loading
                ? 'Accepting invitation...'
                : 'Accept invitation'}

              {!loading && <ArrowRight size={17} />}
            </button>
          </>
        ) : (
          <>
            <p>
              Sign in or create an account using the email
              address that received this invitation.
            </p>

            <Link
              className="auth-submit"
              to={`/login?next=${encodeURIComponent(nextPath || '/dashboard')}`}
            >
              Sign in to accept
              <ArrowRight size={17} />
            </Link>

            <Link
              className="auth-submit"
              to={`/register?next=${encodeURIComponent(nextPath || '/dashboard')}`}
              style={{ marginTop: 12 }}
            >
              Create an account
              <ArrowRight size={17} />
            </Link>
          </>
        )}

        <p className="auth-footer">
          <CheckCircle2
            size={14}
            style={{
              verticalAlign: 'middle',
              marginRight: 5,
            }}
          />
          Invitation access is verified securely.
        </p>
      </section>
    </main>
  )
}

export default AcceptInvitation
