import { useState } from 'react'

import { updateBusiness } from '../../../services/settings'

export function useBusinessSettings({
  businessId,
  businessForm,
  setBusiness,
  setBusinesses,
  setError,
  setMessage,
}) {
  const [businessSaving, setBusinessSaving] =
    useState(false)

  async function handleBusinessSubmit(event) {
    event.preventDefault()

    if (!businessId) {
      return
    }

    try {
      setBusinessSaving(true)
      setError('')
      setMessage('')

      const updated = await updateBusiness(
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

  return {
    businessSaving,
    handleBusinessSubmit,
  }
}
