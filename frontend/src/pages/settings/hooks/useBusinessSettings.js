import { useState } from 'react'

import { updateBusiness as saveBusiness } from '../../../services/settings'

export function useBusinessSettings({
  businessId,
  businessForm,
  updateBusiness,
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

      const updated = await saveBusiness(
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

      updateBusiness(updated)

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
