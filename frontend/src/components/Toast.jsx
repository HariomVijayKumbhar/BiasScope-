import { useEffect } from 'react'

function Toast({ type, message, onClose }) {
  useEffect(() => {
    const timer = setTimeout(onClose, 2500)
    return () => clearTimeout(timer)
  }, [onClose])

  const classes = type === 'success' ? 'bg-green-600' : 'bg-red-600'

  return (
    <div className={`fixed bottom-6 right-6 rounded-lg px-4 py-3 text-sm text-white shadow ${classes}`}>
      {message}
    </div>
  )
}

export default Toast
