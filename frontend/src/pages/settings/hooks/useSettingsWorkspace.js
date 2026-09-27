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

        if (!active) {
          return
        }

        setProfile(profileData)
      } catch (err) {
        if (!active) {
          return
        }

        setError(
          err.response?.data?.detail ||
            'Unable to load settings.',
        )
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
    if (!businessId) {
      return undefined
    }

    let active = true

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

        if (!active) {
          return
        }

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

        updateBusiness(businessData)
      } catch (err) {
        if (!active) {
          return
        }

        setError(
          err.response?.data?.detail ||
            'Unable to load business settings.',
        )
      }
    }

    loadBusinessSettings()

    return () => {
      active = false
    }
  }, [
    businessId,
    setError,
    setMessage,
    updateBusiness,
  ])

  function handleBusinessSelect(event) {
    selectBusiness(event.target.value)
    setMembers([])
    setBusinessForm(emptyBusiness)
    setMessage('')
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
    businessForm,
    setBusinessForm,
    loading:
      businessLoading || loading,
    handleBusinessSelect,
    handleBusinessChange,
    updateBusiness,
  }
}
