import { useState } from 'react'
import { sendChat } from '../services/api'

export function useChat(auditContext) {
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const ask = async (message) => {
    const nextUser = { role: 'user', content: message }
    const history = [...messages, nextUser]
    setMessages(history)
    setLoading(true)
    try {
      const result = await sendChat({
        message,
        audit_context: auditContext,
        history: history.map((m) => ({ role: m.role, content: m.content })),
      })
      setMessages((prev) => [...prev, { role: 'assistant', content: result.reply }])
    } finally {
      setLoading(false)
    }
  }

  const clear = () => setMessages([])

  return { messages, loading, ask, clear }
}
