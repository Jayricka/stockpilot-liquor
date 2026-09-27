import { useState } from 'react'

import SettingsHeader from '../../components/settings/SettingsHeader'
import ProfileSettings from '../../components/settings/ProfileSettings'
import BusinessSettings from '../../components/settings/BusinessSettings'
import TeamSettings from '../../components/settings/TeamSettings'

import { useSettingsWorkspace } from './hooks/useSettingsWorkspace'
import { useProfileSettings } from './hooks/useProfileSettings'
import { useBusinessSettings } from './hooks/useBusinessSettings'

function Settings() {
  const [error, setError] = useState('')
  const [message, setMessage] = useState('')

  const workspace = useSettingsWorkspace({
    setError,
    setMessage,
  })

  const profileSettings = useProfileSettings({
    profile: workspace.profile,
    setProfile: workspace.setProfile,
    setError,
    setMessage,
  })

  const businessSettings =
    useBusinessSettings({
      businessId: workspace.businessId,
      businessForm: workspace.businessForm,
      updateBusiness:
        workspace.updateBusiness,
      setError,
      setMessage,
    })

  if (workspace.loading) {
    return (
      <section className="settings-page">
        <div className="settings-state">
          <h2>Loading settings...</h2>

          <p>
            Preparing your account and business
            settings.
          </p>
        </div>
      </section>
    )
  }

  if (!workspace.profile) {
    return (
      <section className="settings-page">
        <div className="settings-state">
          <h2>Unable to load settings</h2>

          <p>{error}</p>
        </div>
      </section>
    )
  }

  const canEditBusiness =
    workspace.business?.role === 'OWNER' ||
    workspace.business?.role === 'MANAGER'

  return (
    <section className="settings-page">
      <SettingsHeader />

      {workspace.businesses.length > 0 && (
        <div className="settings-business-selector">
          <label>
            Business

            <select
              value={workspace.businessId}
              onChange={
                workspace.handleBusinessSelect
              }
            >
              {workspace.businesses.map(
                (item) => (
                  <option
                    key={item.id}
                    value={item.id}
                  >
                    {item.name}
                  </option>
                ),
              )}
            </select>
          </label>
        </div>
      )}

      {error && (
        <div
          className="settings-error"
          role="alert"
        >
          {error}
        </div>
      )}

      {message && (
        <div className="settings-message">
          {message}
        </div>
      )}

      <div className="settings-grid">
        <ProfileSettings
          profile={workspace.profile}
          form={profileSettings.profileForm}
          saving={
            profileSettings.profileSaving
          }
          onChange={
            profileSettings.handleProfileChange
          }
          onSubmit={
            profileSettings.handleProfileSubmit
          }
        />

        {workspace.business && (
          <BusinessSettings
            business={workspace.business}
            form={workspace.businessForm}
            saving={
              businessSettings.businessSaving
            }
            editable={canEditBusiness}
            onChange={
              workspace.handleBusinessChange
            }
            onSubmit={
              businessSettings.handleBusinessSubmit
            }
          />
        )}

        {workspace.business && (
          <TeamSettings
            members={workspace.members}
          />
        )}
      </div>
    </section>
  )
}

export default Settings
