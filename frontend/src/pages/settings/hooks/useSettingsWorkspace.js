import {
  useEffect,
  useState,
} from 'react'

import { useBusiness } from '../../../context/BusinessContext'

import {
  getBusiness,
  getBusinessMembers,
  getProfile,
} from '../../../services/settings'

const emptyBusiness = {
  name: '',
  business_type: '',
  phone: '',
  email: '',
  address: '',
  license_number: '',
}

function getErrorMessage(error, fallback) {
  return (
    error.response?.data?.detail ||
    fallback
  )
}

export function useSettingsWorkspace({
  setError,
  setMessage,
}) {
  const {
    businesses,
    business,
    businessId: contextBusinessId,
    selectBusiness,
    updateBusiness,
    loading: businessLoading,
  } = useBusiness()

  const businessId = contextBusinessId
    ? String(contextBusinessId)
    : ''

  const [profile, setProfile] =
    useState(null)

  const [members, setMembers] =
    useState([])

  const [businessForm, setBusinessForm] =
    useState(emptyBusiness)

  const [loading, setLoading] =
    useState(true)

  useEffect(() => {
    let active = true

    async function loadProfile() {
      try {
        setLoading(true)
        setError('')

        const profileData = await getProfile()

        if (active) {
          setProfile(profileData)
        }
      } catch (error) {
        if (active) {
          setError(
            getErrorMessage(
              error,
              'Unable to load settings.',
            ),
          )
        }
      } finally {
        if (active) {
          setLoading(false)
        }
      }
    }

    loadProfile()

    return () => {
      active = false
    }
  }, [setError])

  useEffect(() => {
    let active = true

    if (!businessId) {
      return () => {
        active = false
      }
    }

    async function loadBusinessSettings() {
      let businessData

      try {
        businessData = await getBusiness(
          businessId,
        )
      } catch (error) {
        if (active) {
          setError(
            getErrorMessage(
              error,
              'Unable to load business settings.',
            ),
          )
        }

        return
      }

      if (!active) {
        return
      }

      setBusinessForm({
        name: businessData.name || '',
        business_type:
          businessData.business_type || '',
        phone: businessData.phone || '',
        email: businessData.email || '',
        address: businessData.address || '',
        license_number:
          businessData.license_number || '',
      })

      updateBusiness(businessData)

      try {
        const memberData =
          await getBusinessMembers(businessId)

        if (active) {
          setMembers(memberData)
        }
      } catch {
        if (active) {
          setMembers([])
          setError(
            'Business settings loaded, but team members could not be loaded.',
          )
        }
      }
    }

    loadBusinessSettings()

    return () => {
      active = false
    }
  }, [
    businessId,
    setError,
    updateBusiness,
  ])

  function handleBusinessSelect(event) {
    setMembers([])
    setBusinessForm({ ...emptyBusiness })
    setError('')
    setMessage('')
    selectBusiness(event.target.value)
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

  return {
    businesses,
    businessId,
    profile,
    setProfile,
    business,
    members,
    setMembers,
    businessForm,
    setBusinessForm,
    loading:
      businessLoading || loading,
    handleBusinessSelect,
    handleBusinessChange,
    updateBusiness,
  }
}
