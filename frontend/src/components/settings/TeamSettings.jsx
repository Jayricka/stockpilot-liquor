import { useTeamMembers } from '../../pages/settings/hooks/useTeamMembers'

function TeamSettings({
  businessId,
  businessRole,
  currentEmail,
  members,
  setMembers,
  setError,
  setMessage,
}) {
  const team = useTeamMembers({
    businessId,
    members,
    setMembers,
    businessRole,
    setError,
    setMessage,
  })

  return (
    <article className="settings-panel settings-team-panel">
      <header>
        <div>
          <span>TEAM</span>
          <h2>Team members</h2>
          <p>
            Manage who can access this business.
          </p>
        </div>
      </header>

      {team.canManage && (
        <form
          className="settings-team-form"
          onSubmit={team.handleAddMember}
        >
          <label>
            Teammate email
            <input
              type="email"
              value={team.email}
              onChange={(event) =>
                team.setEmail(event.target.value)
              }
              placeholder="colleague@example.com"
              autoComplete="email"
              required
            />
          </label>

          <div className="settings-team-form-actions">
            {team.isOwner && (
              <label>
                Role
                <select
                  value={team.role}
                  onChange={(event) =>
                    team.setRole(event.target.value)
                  }
                >
                  <option value="STAFF">Staff</option>
                  <option value="MANAGER">Manager</option>
                </select>
              </label>
            )}

            <button type="submit" disabled={team.adding}>
              {team.adding
                ? 'Creating invitation...'
                : 'Invite teammate'}
            </button>
          </div>

          <p className="settings-team-hint">
            The invitation expires after seven days.
            Access is granted when the recipient accepts it
            using the invited email address.
          </p>
        </form>
      )}

      {team.invitationToken && (
        <section
          className="settings-invitation-token"
          aria-labelledby="invitation-token-heading"
        >
          <h3 id="invitation-token-heading">
            Invitation link
          </h3>

          <p>
            Share this link with the invited teammate.
            It expires after seven days and must be
            accepted using the invited email address.
          </p>

          <code>{team.invitationLink}</code>

          <div className="settings-team-form-actions">
            <button
              type="button"
              onClick={team.handleCopyInvitationLink}
            >
              Copy invitation link
            </button>

            <button
              type="button"
              className="settings-secondary-button"
              onClick={() => team.setInvitationToken('')}
            >
              Hide link
            </button>
          </div>
        </section>
      )}

      {team.canManage && (
        <section className="settings-pending-invitations">
          <div className="settings-section-heading">
            <h3>Pending invitations</h3>
            <span>{team.invitations.length}</span>
          </div>

          {team.loadingInvitations ? (
            <p className="settings-empty">
              Loading invitations...
            </p>
          ) : team.invitations.length === 0 ? (
            <p className="settings-empty">
              No pending invitations.
            </p>
          ) : (
            <div className="settings-members">
              {team.invitations.map((invitation) => (
                <div
                  className="settings-member"
                  key={invitation.id}
                >
                  <div className="settings-member-details">
                    <strong>{invitation.email}</strong>
                    <span>
                      {invitation.role} · Expires{' '}
                      {new Date(
                        invitation.expires_at,
                      ).toLocaleDateString()}
                    </span>
                  </div>

                  <div className="settings-member-actions">
                    <span className="settings-member-role">
                      Pending
                    </span>

                    <button
                      type="button"
                      className="settings-danger-button"
                      disabled={
                        team.busyInvitationId === invitation.id
                      }
                      onClick={() => {
                        if (
                          window.confirm(
                            `Revoke the invitation for ${invitation.email}?`,
                          )
                        ) {
                          team.handleRevokeInvitation(
                            invitation,
                          )
                        }
                      }}
                    >
                      {team.busyInvitationId === invitation.id
                        ? 'Revoking...'
                        : 'Revoke'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      <section className="settings-active-members">
        <div className="settings-section-heading">
          <h3>Active members</h3>
          <span>{members.length}</span>
        </div>

        {!members.length ? (
          <p className="settings-empty">
            No active team members found.
          </p>
        ) : (
          <div className="settings-members">
            {members.map((member) => {
              const isSelf =
                member.email?.toLowerCase() ===
                currentEmail?.toLowerCase()

              const canManageMember = team.isOwner
                ? member.role !== 'OWNER'
                : businessRole === 'MANAGER' &&
                  member.role === 'STAFF' &&
                  !isSelf

              return (
                <div
                  className="settings-member"
                  key={member.user_id}
                >
                  <div className="settings-member-details">
                    <strong>
                      {member.full_name || 'Unnamed member'}
                      {isSelf ? ' (you)' : ''}
                    </strong>

                    <span>{member.email}</span>
                  </div>

                  <div className="settings-member-actions">
                    {team.isOwner &&
                    member.role !== 'OWNER' ? (
                      <label className="settings-inline-label">
                        <span className="settings-sr-only">
                          Role for {member.email}
                        </span>

                        <select
                          value={member.role}
                          disabled={
                            team.busyUserId === member.user_id
                          }
                          onChange={(event) =>
                            team.handleRoleChange(
                              member,
                              event.target.value,
                            )
                          }
                        >
                          <option value="STAFF">Staff</option>
                          <option value="MANAGER">Manager</option>
                        </select>
                      </label>
                    ) : (
                      <span className="settings-member-role">
                        {member.role}
                      </span>
                    )}

                    {canManageMember && (
                      <button
                        type="button"
                        className="settings-danger-button"
                        disabled={
                          team.busyUserId === member.user_id
                        }
                        onClick={() => {
                          if (
                            window.confirm(
                              `Deactivate ${member.email}'s access to this business?`,
                            )
                          ) {
                            team.handleDeactivate(member)
                          }
                        }}
                      >
                        {team.busyUserId === member.user_id
                          ? 'Saving...'
                          : 'Deactivate'}
                      </button>
                    )}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </section>
    </article>
  )
}

export default TeamSettings
