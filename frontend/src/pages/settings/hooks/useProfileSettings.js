import { useState } from 'react'

import { updateProfile } from '../../../services/settings'

const emptyProfile = {
  first_name: '',
  last_name: '',
}

export function useProfileSettings({
  profile,
  setProfile,
  setError,
  setMessage,
}) {
  const [profileForm, setProfileForm] =
    useState({
      ...emptyProfile,
      first_name: profile?.first_name || '',
      last_name: profile?.last_name || '',
    })

  const [profileSaving, setProfileSaving] =
    useState(false)

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

  async function handleProfileSubmit(event) {
    event.preventDefault()

    try {
      setProfileSaving(true)
      setError('')
      setMessage('')

      const updated = await updateProfile({
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

  return {
    profileForm,
    profileSaving,
    handleProfileChange,
    handleProfileSubmit,
  }
}
