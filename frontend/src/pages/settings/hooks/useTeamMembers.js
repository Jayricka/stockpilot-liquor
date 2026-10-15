import {
  useEffect,
  useState,
} from 'react'

import {
  createBusinessInvitation,
  deactivateBusinessMember,
  getBusinessInvitations,
  revokeBusinessInvitation,
  updateBusinessMember,
} from '../../../services/settings'

function getErrorMessage(error) {
  const data = error.response?.data

  if (typeof data?.detail === 'string') {
    return data.detail
  }

  if (data && typeof data === 'object') {
    const messages = Object.values(data).flat()

    if (messages.length) {
      return String(messages[0])
    }
  }

  return 'Unable to complete the team action.'
}

export function useTeamMembers({
  businessId,
  members,
  setMembers,
  businessRole,
  setError,
  setMessage,
}) {
  const [email, setEmail] = useState('')
  const [role, setRole] = useState('STAFF')
  const [adding, setAdding] = useState(false)
  const [busyUserId, setBusyUserId] = useState(null)
  const [invitations, setInvitations] = useState([])
  const [loadingInvitations, setLoadingInvitations] =
    useState(false)
  const [busyInvitationId, setBusyInvitationId] =
    useState(null)
  const [invitationToken, setInvitationToken] =
    useState('')

  const isOwner = businessRole === 'OWNER'
  const canManage =
    isOwner || businessRole === 'MANAGER'

  const invitationLink = invitationToken
    ? `${window.location.origin}/invitations/accept?token=${encodeURIComponent(invitationToken)}`
    : ''

  useEffect(() => {
    let active = true

    if (!businessId || !canManage) {
      return () => {
        active = false
      }
    }

    async function loadInvitations() {
      try {
        setLoadingInvitations(true)

        const data = await getBusinessInvitations(
          businessId,
        )

        if (active) {
          setInvitations(
            data.filter(
              (item) => item.status === 'PENDING',
            ),
          )
        }
      } catch (error) {
        if (active) {
          setError(getErrorMessage(error))
        }
      } finally {
        if (active) {
          setLoadingInvitations(false)
        }
      }
    }

    loadInvitations()

    return () => {
      active = false
    }
  }, [businessId, canManage, setError])

  async function handleAddMember(event) {
    event.preventDefault()

    if (!businessId || !canManage) return

    try {
      setAdding(true)
      setError('')
      setMessage('')
      setInvitationToken('')

      const response = await createBusinessInvitation(
        businessId,
        {
          email: email.trim(),
          role: isOwner ? role : 'STAFF',
        },
      )

      setInvitations((current) => [
        response.invitation,
        ...current.filter(
          (item) => item.id !== response.invitation.id,
        ),
      ])

      setInvitationToken(response.token || '')
      setEmail('')
      setMessage('Invitation created successfully.')
    } catch (error) {
      setError(getErrorMessage(error))
    } finally {
      setAdding(false)
    }
  }

  async function handleRevokeInvitation(invitation) {
    if (!businessId || !canManage) return

    try {
      setBusyInvitationId(invitation.id)
      setError('')
      setMessage('')

      await revokeBusinessInvitation(
        businessId,
        invitation.id,
      )

      setInvitations((current) =>
        current.filter(
          (item) => item.id !== invitation.id,
        ),
      )

      setMessage('Invitation revoked successfully.')
    } catch (error) {
      setError(getErrorMessage(error))
    } finally {
      setBusyInvitationId(null)
    }
  }

  async function handleCopyInvitationLink() {
    if (!invitationLink) return

    try {
      if (!navigator.clipboard?.writeText) {
        throw new Error('Clipboard unavailable.')
      }

      await navigator.clipboard.writeText(
        invitationLink,
      )

      setMessage('Invitation link copied.')
      setError('')
    } catch {
      setError(
        'Unable to copy automatically. Select and copy the invitation link.',
      )
    }
  }

  async function handleRoleChange(member, nextRole) {
    if (
      !businessId ||
      !isOwner ||
      member.role === 'OWNER' ||
      member.role === nextRole
    ) {
      return
    }

    try {
      setBusyUserId(member.user_id)
      setError('')
      setMessage('')

      const updated = await updateBusinessMember(
        businessId,
        member.user_id,
        { role: nextRole },
      )

      setMembers((current) =>
        current.map((item) =>
          item.user_id === updated.user_id
            ? updated
            : item,
        ),
      )

      setMessage('Member role updated successfully.')
    } catch (error) {
      setError(getErrorMessage(error))
    } finally {
      setBusyUserId(null)
    }
  }

  async function handleDeactivate(member) {
    if (
      !businessId ||
      !canManage ||
      member.role === 'OWNER' ||
      (
        businessRole === 'MANAGER' &&
        member.role !== 'STAFF'
      )
    ) {
      return
    }

    try {
      setBusyUserId(member.user_id)
      setError('')
      setMessage('')

      await deactivateBusinessMember(
        businessId,
        member.user_id,
      )

      setMembers((current) =>
        current.filter(
          (item) => item.user_id !== member.user_id,
        ),
      )

      setMessage('Team member deactivated successfully.')
    } catch (error) {
      setError(getErrorMessage(error))
    } finally {
      setBusyUserId(null)
    }
  }

  return {
    email,
    setEmail,
    role,
    setRole,
    adding,
    busyUserId,
    canManage,
    isOwner,
    members,
    invitations,
    loadingInvitations,
    busyInvitationId,
    invitationToken,
    invitationLink,
    setInvitationToken,
    handleAddMember,
    handleRevokeInvitation,
    handleCopyInvitationLink,
    handleRoleChange,
    handleDeactivate,
  }
}
