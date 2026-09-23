import {
  useEffect,
  useState,
} from 'react'

import {
  getBusinesses,
} from '../../services/dashboard'

import {
  getBusiness,
  getBusinessMembers,
  getProfile,
  updateBusiness,
  updateProfile,
} from '../../services/settings'

import SettingsHeader from '../../components/settings/SettingsHeader'
import ProfileSettings from '../../components/settings/ProfileSettings'
import BusinessSettings from '../../components/settings/BusinessSettings'
import TeamSettings from '../../components/settings/TeamSettings'

const emptyProfile = {
  first_name: '',
  last_name: '',
}

const emptyBusiness = {
  name: '',
  business_type: '',
  phone: '',
  email: '',
  address: '',
  license_number: '',
}

function Settings() {
  const [businesses, setBusinesses] =
    useState([])

  const [businessId, setBusinessId] =
    useState('')

  const [profile, setProfile] =
    useState(null)

  const [business, setBusiness] =
    useState(null)

  const [members, setMembers] =
    useState([])

  const [profileForm, setProfileForm] =
    useState(emptyProfile)

  const [businessForm, setBusinessForm] =
    useState(emptyBusiness)

  const [loading, setLoading] =
    useState(true)

  const [profileSaving, setProfileSaving] =
    useState(false)

  const [businessSaving, setBusinessSaving] =
    useState(false)

  const [error, setError] =
    useState('')

  const [message, setMessage] =
    useState('')

  useEffect(() => {
    async function loadInitialData() {
      try {
        setLoading(true)
        setError('')

        const [
          profileData,
          businessData,
        ] = await Promise.all([
          getProfile(),
          getBusinesses(),
        ])

        const availableBusinesses =
          Array.isArray(businessData)
            ? businessData
            : businessData?.results || []

        setProfile(profileData)

        setProfileForm({
          first_name:
            profileData.first_name || '',
          last_name:
            profileData.last_name || '',
        })

        setBusinesses(availableBusinesses)

        if (availableBusinesses.length) {
          setBusinessId(
            String(
              availableBusinesses[0].id,
            ),
          )
        }
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Unable to load settings.',
        )
      } finally {
        setLoading(false)
      }
    }

    loadInitialData()
  }, [])

  useEffect(() => {
    if (!businessId) {
      return
    }

    async function loadBusinessSettings() {
      try {
        setError('')
        setMessage('')

        const [
          businessData,
          memberData,
        ] = await Promise.all([
          getBusiness(businessId),
          getBusinessMembers(businessId),
        ])

        setBusiness(businessData)

        setBusinessForm({
          name: businessData.name || '',
          business_type:
            businessData.business_type || '',
          phone: businessData.phone || '',
          email: businessData.email || '',
          address:
            businessData.address || '',
          license_number:
            businessData.license_number || '',
        })

        setMembers(memberData)
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            'Unable to load business settings.',
        )
      }
    }

    loadBusinessSettings()
  }, [businessId])

  function handleBusinessSelect(event) {
    const nextBusinessId =
      event.target.value

    setBusinessId(nextBusinessId)
    setBusiness(null)
    setMembers([])
    setMessage('')
  }

  function handleProfileChange(event) {
    const {
      name,
      value,
    } = event.target

    setProfileForm((current) => ({
      ...current,
      [name]: value,
    }))
  }

  function handleBusinessChange(event) {
    const {
      name,
      value,
    } = event.target

    setBusinessForm((current) => ({
      ...current,
      [name]: value,
    }))
  }

  async function handleProfileSubmit(event) {
    event.preventDefault()

    try {
      setProfileSaving(true)
      setError('')
      setMessage('')

      const updated =
        await updateProfile({
          first_name:
            profileForm.first_name.trim(),
          last_name:
            profileForm.last_name.trim(),
        })

      setProfile(updated)

      setProfileForm({
        first_name:
          updated.first_name || '',
        last_name:
          updated.last_name || '',
      })

      setMessage(
        'Profile updated successfully.',
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to update profile.',
      )
    } finally {
      setProfileSaving(false)
    }
  }

  async function handleBusinessSubmit(event) {
    event.preventDefault()

    if (!businessId) {
      return
    }

    try {
      setBusinessSaving(true)
      setError('')
      setMessage('')

      const updated =
        await updateBusiness(
          businessId,
          {
            name:
              businessForm.name.trim(),
            business_type:
              businessForm.business_type.trim(),
            phone:
              businessForm.phone.trim(),
            email:
              businessForm.email.trim(),
            address:
              businessForm.address.trim(),
            license_number:
              businessForm.license_number.trim(),
          },
        )

      setBusiness(updated)

      setBusinesses((current) =>
        current.map((item) =>
          item.id === Number(businessId)
            ? updated
            : item,
        ),
      )

      setMessage(
        'Business information updated successfully.',
      )
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          'Unable to update business.',
      )
    } finally {
      setBusinessSaving(false)
    }
  }

  if (loading) {
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

  if (!profile) {
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
    business?.role === 'OWNER' ||
    business?.role === 'MANAGER'

  return (
    <section className="settings-page">
      <SettingsHeader />

      {businesses.length > 0 && (
        <div className="settings-business-selector">
          <label>
            Business

            <select
              value={businessId}
              onChange={
                handleBusinessSelect
              }
            >
              {businesses.map((item) => (
                <option
                  key={item.id}
                  value={item.id}
                >
                  {item.name}
                </option>
              ))}
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
          profile={profile}
          form={profileForm}
          saving={profileSaving}
          onChange={handleProfileChange}
          onSubmit={handleProfileSubmit}
        />

        {business && (
          <BusinessSettings
            business={business}
            form={businessForm}
            saving={businessSaving}
            editable={canEditBusiness}
            onChange={handleBusinessChange}
            onSubmit={handleBusinessSubmit}
          />
        )}

        {business && (
          <TeamSettings
            members={members}
          />
        )}
      </div>
    </section>
  )
}

export default Settings
