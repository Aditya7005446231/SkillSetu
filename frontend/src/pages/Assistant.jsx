import { Bot, CheckCircle2, Loader2, Send, Sparkles, User } from 'lucide-react'
import { useState, useRef, useEffect } from 'react'
import JobCard from '../components/JobCard'
import { sendChatMessage } from '../services/opportunities'

const QUICK_PROMPTS = [
  'Show remote internships only',
  'Jobs in Bangalore with React and Python',
  'Internships with minimum 75% match',
  'Focus on Frontend Developer roles',
  'Clear all filters'
]

function Assistant() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      sender: 'assistant',
      text: 'Hi there! I am your SkillSetu Career Copilot. Ask me to refine your job search, filter by location or remote mode, focus on specific skills, or help bridge your skill gaps!',
      badges: [],
      jobs: []
    }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const chatEndRef = useRef(null)

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const handleSend = async (textToSend) => {
    const userText = (textToSend || input).trim()
    if (!userText || loading) return

    setInput('')
    setError('')

    const userMessageId = Date.now()
    setMessages((prev) => [
      ...prev,
      { id: userMessageId, sender: 'user', text: userText }
    ])

    setLoading(true)
    try {
      const response = await sendChatMessage(userText)
      const assistantMessage = {
        id: Date.now() + 1,
        sender: 'assistant',
        text: response.reply || 'Preferences updated and recommendations refreshed.',
        badges: response.filters_applied || [],
        jobs: response.recommendations || []
      }
      setMessages((prev) => [...prev, assistantMessage])
    } catch (err) {
      console.error('Chat error:', err)
      const errorMsg = err.response?.data?.detail || err.message || 'Something went wrong.'
      setError(errorMsg)
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          sender: 'assistant',
          text: `Sorry, I encountered an issue: ${errorMsg}`,
          isError: true
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="assistant-page">
      <section className="assistant-intro">
        <div className="assistant-avatar">
          <Sparkles size={25} />
        </div>
        <div>
          <h2>Your Career Copilot</h2>
          <p>
            Converse with your AI agent to refine job filters, set location preferences, and see updated opportunities instantly.
          </p>
        </div>
      </section>

      <section className="chat-panel panel">
        <div className="chat-messages-container" style={{ maxHeight: '600px', overflowY: 'auto', paddingRight: '8px' }}>
          {messages.map((msg) => (
            <div
              key={msg.id}
              className={`chat-message ${msg.sender === 'user' ? 'user-message' : 'assistant-message'}`}
              style={{ marginBottom: '1.25rem' }}
            >
              <span className={msg.sender === 'user' ? 'avatar' : 'chat-icon'}>
                {msg.sender === 'user' ? <User size={16} /> : <Bot size={17} />}
              </span>
              <div style={{ flex: 1 }}>
                <strong>{msg.sender === 'user' ? 'You' : 'SkillSetu Copilot'}</strong>
                <p style={{ marginTop: '0.25rem', whiteSpace: 'pre-wrap' }}>{msg.text}</p>

                {msg.badges && msg.badges.length > 0 && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.6rem' }}>
                    {msg.badges.map((b, idx) => (
                      <span
                        key={idx}
                        style={{
                          fontSize: '0.75rem',
                          background: 'var(--brand-surface, #e0f2fe)',
                          color: 'var(--brand-primary, #0284c7)',
                          padding: '0.2rem 0.55rem',
                          borderRadius: '9999px',
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '0.25rem',
                          fontWeight: 500
                        }}
                      >
                        <CheckCircle2 size={12} /> {b}
                      </span>
                    ))}
                  </div>
                )}

                {msg.jobs && msg.jobs.length > 0 && (
                  <div style={{ marginTop: '1rem' }}>
                    <div style={{ fontSize: '0.825rem', fontWeight: 600, color: 'var(--text-secondary, #64748b)', marginBottom: '0.5rem' }}>
                      {msg.jobs.length} Matching Opportunities Refreshed:
                    </div>
                    <div className="jobs-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))', gap: '0.75rem' }}>
                      {msg.jobs.slice(0, 4).map((job) => (
                        <JobCard key={job.job_id} job={job} />
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="chat-message assistant-message" style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span className="chat-icon"><Bot size={17} /></span>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#64748b' }}>
                <Loader2 size={16} className="animate-spin" />
                <span>Refining preferences & matching jobs...</span>
              </div>
            </div>
          )}

          <div ref={chatEndRef} />
        </div>

        <div className="prompt-grid" style={{ marginTop: '1rem' }}>
          {QUICK_PROMPTS.map((promptText, i) => (
            <button
              key={i}
              type="button"
              disabled={loading}
              onClick={() => handleSend(promptText)}
              style={{ fontSize: '0.82rem', textAlign: 'left' }}
            >
              {promptText}
            </button>
          ))}
        </div>

        <form
          className="chat-input"
          style={{ marginTop: '1rem' }}
          onSubmit={(e) => {
            e.preventDefault()
            handleSend()
          }}
        >
          <input
            value={input}
            disabled={loading}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Tell your copilot e.g. 'Show me remote React internships in Bangalore'..."
          />
          <button aria-label="Send message" type="submit" disabled={loading || !input.trim()}>
            {loading ? <Loader2 size={18} className="animate-spin" /> : <Send size={18} />}
          </button>
        </form>
      </section>
    </div>
  )
}

export default Assistant
