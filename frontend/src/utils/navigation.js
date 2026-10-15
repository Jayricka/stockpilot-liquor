export function getSafeNextPath(value) {
  if (
    typeof value !== 'string' ||
    !value.startsWith('/') ||
    value.startsWith('//') ||
    value.includes('\\')
  ) {
    return null
  }

  try {
    const url = new URL(
      value,
      window.location.origin,
    )

    if (url.origin !== window.location.origin) {
      return null
    }

    return `${url.pathname}${url.search}${url.hash}`
  } catch {
    return null
  }
}
