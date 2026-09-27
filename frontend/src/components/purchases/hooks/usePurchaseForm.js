import { useState } from 'react'

function getToday() {
  return new Date()
    .toISOString()
    .split('T')[0]
}

const emptyItem = {
  product: '',
  quantity: '',
  unit_cost: '',
}

const emptyForm = {
  supplier: '',
  reference_number: '',
  purchase_date: getToday(),
  notes: '',
  items: [{ ...emptyItem }],
}

export function usePurchaseForm() {
  const [form, setForm] = useState(emptyForm)

  function resetForm() {
    setForm({
      ...emptyForm,
      purchase_date: getToday(),
      items: [{ ...emptyItem }],
    })
  }

  function handleChange(event) {
    const {
      name,
      value,
    } = event.target

    setForm((current) => ({
      ...current,
      [name]: value,
    }))
  }

  function handleItemChange(
    index,
    field,
    value,
  ) {
    setForm((current) => ({
      ...current,
      items: current.items.map(
        (item, itemIndex) =>
          itemIndex === index
            ? {
                ...item,
                [field]: value,
              }
            : item,
      ),
    }))
  }

  function addItem() {
    setForm((current) => ({
      ...current,
      items: [
        ...current.items,
        { ...emptyItem },
      ],
    }))
  }

  function removeItem(index) {
    setForm((current) => ({
      ...current,
      items: current.items.filter(
        (_, itemIndex) =>
          itemIndex !== index,
      ),
    }))
  }

  return {
    form,
    setForm,
    resetForm,
    handleChange,
    handleItemChange,
    addItem,
    removeItem,
  }
}
