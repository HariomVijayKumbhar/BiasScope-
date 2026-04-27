import { useState } from 'react'
import { useChat } from '../hooks/useChat'

function ChatPanel({ auditContext }) {
  const [message, setMessage] = useState('')
  const [open, setOpen] = useState(false)
  const { messages, loading, ask, clear } = useChat(auditContext)

  const starterQuestions = [
    'What is the biggest risk in my dataset?',
    'Which metric failed and why?',
    'What should I fix first?',
    'Is my dataset safe to use?',
  ]

  const onSend = async () => {
    if (!message.trim()) return
    const prompt = message.trim()
    setMessage('')
    await ask(prompt)
  }

  return (
    <div className="fixed bottom-6 right-6 z-30">
      <button className="rounded-full bg-primary px-4 py-3 text-sm font-semibold text-white" onClick={() => setOpen((prev) => !prev)}>
        Ask BiasScope
      </button>
      {open && (
        <div className="mt-3 flex h-[520px] w-[380px] flex-col rounded-xl border border-border bg-white shadow-xl">
          <div className="flex items-center justify-between border-b border-border p-3">
            <h4 className="font-semibold">Audit Assistant</h4>
            <button className="text-xs text-slate-500" onClick={clear}>Clear Chat</button>
          </div>
          <div className="space-y-3 overflow-y-auto p-3 text-sm">
            {starterQuestions.map((q) => (
              <button key={q} className="mr-2 rounded-full border border-border px-2 py-1 text-xs" onClick={() => ask(q)}>{q}</button>
            ))}
            {messages.map((msg, idx) => (
              <div key={idx} className={`max-w-[85%] rounded-lg px-3 py-2 ${msg.role === 'user' ? 'ml-auto bg-primary text-white' : 'bg-slate-100 text-slate-800'}`}>
                {msg.content}
              </div>
            ))}
            {loading && <div className="text-xs text-slate-500">BiasScope is typing...</div>}
          </div>
          <div className="border-t border-border p-3">
            <div className="flex gap-2">
              <input value={message} onChange={(e) => setMessage(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && onSend()} className="flex-1 rounded border border-border px-3 py-2 text-sm" placeholder="Ask about this audit" />
              <button className="rounded bg-primary px-3 py-2 text-sm text-white" onClick={onSend}>Send</button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default ChatPanel
