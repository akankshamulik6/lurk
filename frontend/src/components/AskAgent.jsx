import { useState } from 'react'
import api from '../api'

function AskAgent() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const handleAsk = async () => {
    if (!question.trim()) return
    const userQuestion = question.trim()
    setMessages(prev => [...prev, { role: 'user', text: userQuestion }])
    setQuestion('')
    setLoading(true)

    try {
      const res = await api.post('/ask', { question: userQuestion })
      setMessages(prev => [...prev, { role: 'agent', text: res.data.answer }])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'agent', text: 'Something went wrong. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleAsk()
  }

  return (
    <div className="border border-accent/40 p-6 max-w-2xl mb-8">
      <div className="text-xs tracking-widest text-accent border-b border-accent/40 pb-3 mb-4">
        ASK THE AGENT
      </div>

      {messages.length > 0 && (
        <div className="space-y-4 mb-4 max-h-96 overflow-y-auto">
          {messages.map((msg, i) => (
            <div key={i}>
              <div className="text-xs tracking-widest text-accent mb-1">
                {msg.role === 'user' ? 'YOU' : 'LURK'}
              </div>
              <p className="text-sm text-line/90 leading-relaxed">{msg.text}</p>
            </div>
          ))}
          {loading && (
            <div>
              <div className="text-xs tracking-widest text-accent mb-1">LURK</div>
              <p className="text-xs tracking-widest text-accent/60">THINKING...</p>
            </div>
          )}
        </div>
      )}

      <div className="flex gap-2">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="e.g. Is 118.25.6.39 malicious? Tell me about CVE-2024-3094"
          className="flex-1 bg-transparent border border-accent/40 px-4 py-2 text-sm tracking-wide placeholder:text-accent/40 focus:outline-none focus:border-accent"
        />
        <button
          onClick={handleAsk}
          disabled={loading}
          className="border border-accent/40 px-4 py-2 text-xs tracking-widest hover:border-accent hover:text-accent transition-colors disabled:opacity-40"
        >
          ASK
        </button>
      </div>
    </div>
  )
}

export default AskAgent