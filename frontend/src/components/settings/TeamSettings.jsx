function TeamSettings({ members }) {
  return (
    <article className="settings-panel">
      <header>
        <div>
          <span>TEAM</span>

          <h2>Team members</h2>

          <p>
            People who have access to this business.
          </p>
        </div>
      </header>

      {!members.length ? (
        <p className="settings-empty">
          No active team members found.
        </p>
      ) : (
        <div className="settings-members">
          {members.map((member) => (
            <div
              className="settings-member"
              key={member.user_id}
            >
              <div>
                <strong>
                  {member.full_name ||
                    'Unnamed member'}
                </strong>

                <span>
                  {member.email}
                </span>
              </div>

              <span className="settings-member-role">
                {member.role}
              </span>
            </div>
          ))}
        </div>
      )}
    </article>
  )
}

export default TeamSettings
