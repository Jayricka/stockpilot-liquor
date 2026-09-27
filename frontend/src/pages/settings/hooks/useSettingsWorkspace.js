import {
  useEffect,
  useState,
} from 'react'

import { getBusinesses } from '../../../services/dashboard'

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

  const [businessForm, setBusinessForm] =
    useState(emptyBusiness)

  const [loading, setLoading] =
    useState(true)

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
  }, [setError])

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
  }, [businessId, setError, setMessage])

  function handleBusinessSelect(event) {
    const nextBusinessId =
      event.target.value

    setBusinessId(nextBusinessId)
    setBusiness(null)
    setMembers([])
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
    setBusinesses,
    businessId,
    profile,
    setProfile,
    business,
    setBusiness,
    members,
    businessForm,
    setBusinessForm,
    loading,
    handleBusinessSelect,
    handleBusinessChange,
  }
}
