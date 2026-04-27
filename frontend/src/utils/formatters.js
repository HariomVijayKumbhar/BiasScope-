export const formatNumber = (value, digits = 4) => {
  const num = Number(value)
  if (Number.isNaN(num)) {
    return '-'
  }
  return num.toFixed(digits)
}

export const bytesToMb = (bytes) => `${(bytes / (1024 * 1024)).toFixed(2)} MB`

export const severityClasses = {
  critical: 'bg-red-100 text-red-700',
  high: 'bg-orange-100 text-orange-700',
  medium: 'bg-yellow-100 text-yellow-700',
  low: 'bg-blue-100 text-blue-700',
}
