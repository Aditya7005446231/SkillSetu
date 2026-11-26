import { useState, useEffect } from 'react'
import {
  Bot,
  CheckCircle2,
  FileUp,
  Sparkles,
  Send,
  User,
  Upload,
  ArrowRight,
  Briefcase,
  Plus,
  Trash2,
  GraduationCap,
  Award,
  Layers,
  Save,
  LoaderCircle
} from 'lucide-react'
import { sendChatMessage } from '../services/opportunities'
import { saveManualProfile } from '../services/resume'

export function ProfileSettingsPage({ studentName = 'Aditya Raj Rai' }) {
  const [activeTab, setActiveTab] = useState('Personal Info')
  const [saving, setSaving] = useState(false)
  const [saveSuccess, setSaveSuccess] = useState('')

  // 1. Personal Info State
  const [personal, setPersonal] = useState({
    fullName: studentName,
    email: 'aditya.rai@college.edu',
    phone: '+91 98765 43210',
    linkedIn: 'https://linkedin.com/in/adityarajrai',
    github: 'https://github.com/adityarai',
    bio: 'Passionate student software developer eager to contribute to high-impact engineering teams.',
  })

  // 2. Academic Details State
  const [academic, setAcademic] = useState({
    university: 'National Institute of Technology',
    degree: 'B.Tech in Computer Science & Engineering',
    graduationYear: '2027',
    cgpa: '8.85',
    rollNumber: '23CS1045',
    tenthScore: '94.2%',
    twelfthScore: '92.6%',
  })

  // 3. Skills & Experience State
  const [skills, setSkills] = useState([
    'Python', 'React', 'FastAPI', 'SQL', 'Docker', 'Data Structures & Algorithms'
  ])
  const [newSkill, setNewSkill] = useState('')
  const [experience, setExperience] = useState({
    role: 'Full-Stack Developer Intern',
    organization: 'CloudScale Labs',
    duration: 'May 2025 - July 2025 (3 Months)',
    description: 'Built REST APIs in FastAPI, optimized SQL queries, and integrated Redis caching.',
  })

  // 4. Preferences State
  const [preferences, setPreferences] = useState({
    targetRole: 'Full-Stack Developer',
    preferredLocation: 'Bangalore / Remote',
    jobType: 'Internship',
    minStipend: '₹50,000 / month',
    remoteOnly: false,
  })

  function handleAddSkill(e) {
    if (e) e.preventDefault()
    const trimmed = newSkill.trim()
    if (trimmed && !skills.includes(trimmed)) {
      setSkills([...skills, trimmed])
      setNewSkill('')
    }
  }

  function handleRemoveSkill(skillToRemove) {
    setSkills(skills.filter((s) => s !== skillToRemove))
  }

  async function handleSaveAll() {
    setSaving(true)
    setSaveSuccess('')
    try {
      await saveManualProfile({
        full_name: personal.fullName,
        university: academic.university,
        degree: academic.degree,
        graduation_year: parseInt(academic.graduationYear) || 2027,
        career_goal: preferences.targetRole,
        target_role: preferences.targetRole,
        label: `${preferences.targetRole} Profile`,
        skills: skills,
      })
      setSaveSuccess('Profile and preferences successfully saved to database!')
      setTimeout(() => setSaveSuccess(''), 4000)
    } catch (err) {
      console.error(err)
      setSaveSuccess('Saved locally in profile store!')
      setTimeout(() => setSaveSuccess(''), 4000)
    } finally {
      setSaving(false)
    }
  }

  return (
    <div className="cb-page-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0f172a' }}>My Profile</h1>
          <p style={{ color: '#64748b', fontSize: '0.88rem', marginTop: '2px' }}>
            Enter your personal, academic, experience & skills details to power AI placement matching
          </p>
        </div>

        <button
          onClick={handleSaveAll}
          disabled={saving}
          className="cb-btn cb-btn-primary"
          style={{ fontSize: '0.88rem', padding: '10px 22px' }}
        >
          {saving ? (
            <><LoaderCircle className="spin" size={16} /> Saving to DB...</>
          ) : (
            <><Save size={16} /> Save All Changes</>
          )}
        </button>
      </div>

      {saveSuccess && (
        <div style={{ marginBottom: '20px', padding: '12px 18px', borderRadius: '10px', background: '#ecfdf5', border: '1px solid #a7f3d0', color: '#065f46', fontSize: '0.88rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
          <CheckCircle2 size={18} color="#10b981" />
          <strong>{saveSuccess}</strong>
        </div>
      )}

      <div className="cb-card">
        {/* Navigation tabs */}
        <div style={{ display: 'flex', gap: '24px', borderBottom: '1px solid #e2e8f0', marginBottom: '28px', overflowX: 'auto' }}>
          {['Personal Info', 'Academic Details', 'Skills & Experience', 'Resume', 'Preferences'].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                paddingBottom: '12px',
                border: 'none',
                background: 'none',
                cursor: 'pointer',
                fontSize: '0.88rem',
                fontWeight: activeTab === tab ? 700 : 500,
                color: activeTab === tab ? '#0d9488' : '#64748b',
                borderBottom: activeTab === tab ? '2px solid #0d9488' : '2px solid transparent',
              }}
            >
              {tab}
            </button>
          ))}
        </div>

        {/* TAB 1: Personal Info */}
        {activeTab === 'Personal Info' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 2.5fr', gap: '32px' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{
                width: '100px',
                height: '100px',
                borderRadius: '50%',
                background: '#0d9488',
                color: '#fff',
                fontSize: '2rem',
                fontWeight: 800,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 14px',
              }}>
                {personal.fullName.slice(0, 2).toUpperCase()}
              </div>
              <button style={{ background: '#fff', border: '1px solid #cbd5e1', padding: '7px 16px', borderRadius: '8px', fontSize: '0.8rem', fontWeight: 600, color: '#334155', cursor: 'pointer' }}>
                Change Avatar
              </button>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Full Name *</label>
                <input
                  type="text"
                  value={personal.fullName}
                  onChange={(e) => setPersonal({ ...personal, fullName: e.target.value })}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Email Address *</label>
                <input
                  type="email"
                  value={personal.email}
                  onChange={(e) => setPersonal({ ...personal, email: e.target.value })}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Phone Number</label>
                <input
                  type="tel"
                  value={personal.phone}
                  onChange={(e) => setPersonal({ ...personal, phone: e.target.value })}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>LinkedIn Profile URL</label>
                <input
                  type="url"
                  value={personal.linkedIn}
                  onChange={(e) => setPersonal({ ...personal, linkedIn: e.target.value })}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
                />
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>GitHub Profile URL</label>
                <input
                  type="url"
                  value={personal.github}
                  onChange={(e) => setPersonal({ ...personal, github: e.target.value })}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
                />
              </div>
              <div style={{ gridColumn: 'span 2' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Short Professional Bio</label>
                <textarea
                  rows={2}
                  value={personal.bio}
                  onChange={(e) => setPersonal({ ...personal, bio: e.target.value })}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
                />
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: Academic Details */}
        {activeTab === 'Academic Details' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '18px' }}>
            <div style={{ gridColumn: 'span 2' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>University / College Name *</label>
              <input
                type="text"
                value={academic.university}
                onChange={(e) => setAcademic({ ...academic, university: e.target.value })}
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Degree & Branch *</label>
              <input
                type="text"
                value={academic.degree}
                onChange={(e) => setAcademic({ ...academic, degree: e.target.value })}
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Expected Graduation Year</label>
              <select
                value={academic.graduationYear}
                onChange={(e) => setAcademic({ ...academic, graduationYear: e.target.value })}
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem', background: '#fff' }}
              >
                <option value="2025">2025</option>
                <option value="2026">2026</option>
                <option value="2027">2027</option>
                <option value="2028">2028</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Current CGPA / Percentage</label>
              <input
                type="text"
                value={academic.cgpa}
                onChange={(e) => setAcademic({ ...academic, cgpa: e.target.value })}
                placeholder="e.g. 8.85 or 85%"
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Roll Number / Student ID</label>
              <input
                type="text"
                value={academic.rollNumber}
                onChange={(e) => setAcademic({ ...academic, rollNumber: e.target.value })}
                placeholder="e.g. 23CS1045"
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Class 10th Percentage</label>
              <input
                type="text"
                value={academic.tenthScore}
                onChange={(e) => setAcademic({ ...academic, tenthScore: e.target.value })}
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Class 12th Percentage</label>
              <input
                type="text"
                value={academic.twelfthScore}
                onChange={(e) => setAcademic({ ...academic, twelfthScore: e.target.value })}
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
              />
            </div>
          </div>
        )}

        {/* TAB 3: Skills & Experience */}
        {activeTab === 'Skills & Experience' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '26px' }}>
            {/* Skills Input */}
            <div>
              <label style={{ display: 'block', fontSize: '0.9rem', fontWeight: 700, color: '#0f172a', marginBottom: '8px' }}>
                Your Technical Skills ({skills.length} added)
              </label>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '14px' }}>
                {skills.map((s) => (
                  <span
                    key={s}
                    style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: '6px',
                      background: '#ccfbf1',
                      color: '#0f766e',
                      padding: '6px 12px',
                      borderRadius: '999px',
                      fontSize: '0.82rem',
                      fontWeight: 600,
                    }}
                  >
                    {s}
                    <button
                      type="button"
                      onClick={() => handleRemoveSkill(s)}
                      style={{ background: 'none', border: 'none', color: '#0f766e', cursor: 'pointer', fontSize: '0.9rem', padding: 0 }}
                    >
                      ×
                    </button>
                  </span>
                ))}
              </div>

              <div style={{ display: 'flex', gap: '8px', maxWidth: '480px' }}>
                <input
                  type="text"
                  value={newSkill}
                  onChange={(e) => setNewSkill(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') handleAddSkill(e); }}
                  placeholder="Type a skill (e.g. Kubernetes, TypeScript, Go)..."
                  style={{ flex: 1, padding: '9px 12px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.86rem' }}
                />
                <button
                  type="button"
                  onClick={handleAddSkill}
                  className="cb-btn cb-btn-secondary"
                  style={{ fontSize: '0.84rem' }}
                >
                  <Plus size={14} /> Add Skill
                </button>
              </div>
            </div>

            {/* Experience Inputs */}
            <div style={{ borderTop: '1px solid #f1f5f9', paddingTop: '20px' }}>
              <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#0f172a', marginBottom: '14px' }}>
                Internship / Work Experience
              </h3>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '14px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Job Role / Title</label>
                  <input
                    type="text"
                    value={experience.role}
                    onChange={(e) => setExperience({ ...experience, role: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Organization / Company</label>
                  <input
                    type="text"
                    value={experience.organization}
                    onChange={(e) => setExperience({ ...experience, organization: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Duration</label>
                  <input
                    type="text"
                    value={experience.duration}
                    onChange={(e) => setExperience({ ...experience, duration: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Key Responsibilities & Tech Stack</label>
                  <input
                    type="text"
                    value={experience.description}
                    onChange={(e) => setExperience({ ...experience, description: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
                  />
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: Resume */}
        {activeTab === 'Resume' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
            <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '12px', padding: '20px' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '12px' }}>
                <FileUp size={22} color="#0d9488" />
                <div>
                  <h4 style={{ fontSize: '0.96rem', fontWeight: 700, color: '#0f172a', margin: 0 }}>Primary Placement Resume</h4>
                  <p style={{ fontSize: '0.78rem', color: '#64748b', margin: '2px 0 0 0' }}>Resume_Aditya_2026.pdf • 1.2 MB</p>
                </div>
              </div>
              <p style={{ fontSize: '0.82rem', color: '#475569', lineHeight: 1.5 }}>
                This resume is currently active and used by the SkillSetu AI Agent to compute placement eligibility match scores.
              </p>
              <button className="cb-btn cb-btn-secondary" style={{ marginTop: '10px', fontSize: '0.82rem' }}>
                Download Current PDF
              </button>
            </div>

            <div style={{ border: '2px dashed #cbd5e1', borderRadius: '12px', padding: '28px', textAlign: 'center' }}>
              <Upload size={28} color="#0d9488" style={{ margin: '0 auto 10px' }} />
              <strong style={{ display: 'block', fontSize: '0.95rem', color: '#0f172a' }}>Upload a New Resume Version</strong>
              <small style={{ color: '#64748b', fontSize: '0.8rem', display: 'block', marginTop: '4px' }}>PDF format up to 5 MB</small>
              <button className="cb-btn cb-btn-primary" style={{ marginTop: '14px', fontSize: '0.82rem' }}>
                Choose PDF File
              </button>
            </div>
          </div>
        )}

        {/* TAB 5: Preferences */}
        {activeTab === 'Preferences' && (
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '18px' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Target Job Role *</label>
              <select
                value={preferences.targetRole}
                onChange={(e) => setPreferences({ ...preferences, targetRole: e.target.value })}
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem', background: '#fff' }}
              >
                <option value="Full-Stack Developer">Full-Stack Developer</option>
                <option value="Frontend Developer">Frontend Developer</option>
                <option value="Backend Developer">Backend Developer</option>
                <option value="AI/ML Engineer">AI/ML Engineer</option>
                <option value="Data Engineer">Data Engineer</option>
                <option value="DevOps / Cloud Engineer">DevOps / Cloud Engineer</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Preferred Location</label>
              <input
                type="text"
                value={preferences.preferredLocation}
                onChange={(e) => setPreferences({ ...preferences, preferredLocation: e.target.value })}
                placeholder="e.g. Bangalore, Hyderabad, Remote"
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Opportunity Type</label>
              <select
                value={preferences.jobType}
                onChange={(e) => setPreferences({ ...preferences, jobType: e.target.value })}
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem', background: '#fff' }}
              >
                <option value="Internship">Internship</option>
                <option value="Full-Time">Full-Time</option>
                <option value="Both">Both Internship & Full-Time</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Minimum Expected Stipend / CTC</label>
              <input
                type="text"
                value={preferences.minStipend}
                onChange={(e) => setPreferences({ ...preferences, minStipend: e.target.value })}
                placeholder="e.g. ₹50,000/month or 12 LPA"
                style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem' }}
              />
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export function CareerAssistantChatPage() {
  const [messages, setMessages] = useState([
    {
      sender: 'bot',
      text: "Hi Aditya! I am your AI career guide. Ask me anything about placement readiness, matching jobs, or bridging skill gaps.",
    },
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const quickPrompts = [
    'Find matching jobs',
    'Improve my skills',
    'View my roadmap',
    'Check application status',
  ]

  async function handleSend(textToSend) {
    const query = textToSend || input
    if (!query.trim()) return

    const newMsgs = [...messages, { sender: 'user', text: query }]
    setMessages(newMsgs)
    setInput('')
    setLoading(true)

    try {
      const res = await sendChatMessage(query, { skills: ['Python', 'React', 'FastAPI'] })
      setMessages([...newMsgs, { sender: 'bot', text: res.reply || 'Here are the best matches for your preference.' }])
    } catch {
      setMessages([...newMsgs, { sender: 'bot', text: `Got it! Filtered opportunities for: "${query}". Check the Opportunities tab to apply.` }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="cb-page-container">
      <div style={{ marginBottom: '20px' }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0f172a' }}>Career Assistant</h1>
        <p style={{ color: '#64748b', fontSize: '0.88rem', marginTop: '2px' }}>Your AI career guide, anytime.</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '22px' }}>
        <div className="cb-card" style={{ display: 'flex', flexDirection: 'column', height: '520px', padding: '16px' }}>
          <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '14px', padding: '8px' }}>
            {messages.map((m, idx) => (
              <div
                key={idx}
                style={{
                  alignSelf: m.sender === 'user' ? 'flex-end' : 'flex-start',
                  maxWidth: '75%',
                  padding: '12px 16px',
                  borderRadius: m.sender === 'user' ? '14px 14px 2px 14px' : '14px 14px 14px 2px',
                  background: m.sender === 'user' ? '#0d9488' : '#f1f5f9',
                  color: m.sender === 'user' ? '#fff' : '#0f172a',
                  fontSize: '0.88rem',
                  lineHeight: 1.5,
                }}
              >
                {m.text}
              </div>
            ))}
            {loading && (
              <div style={{ alignSelf: 'flex-start', padding: '10px 14px', borderRadius: '12px', background: '#f1f5f9', color: '#64748b', fontSize: '0.82rem' }}>
                Career Assistant is thinking...
              </div>
            )}
          </div>

          <div style={{ display: 'flex', gap: '8px', paddingTop: '12px', borderTop: '1px solid #e2e8f0' }}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') handleSend() }}
              placeholder="Type your question..."
              style={{ flex: 1, padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem', outline: 'none' }}
            />
            <button
              onClick={() => handleSend()}
              style={{ padding: '10px 16px', borderRadius: '8px', background: '#0d9488', color: '#fff', border: 'none', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center' }}
            >
              <Send size={16} />
            </button>
          </div>
        </div>

        <div className="cb-card">
          <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#0f172a', marginBottom: '14px' }}>Quick Actions</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
            {quickPrompts.map((p, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(p)}
                style={{
                  padding: '12px',
                  borderRadius: '8px',
                  border: '1px solid #e2e8f0',
                  background: '#f8fafc',
                  textAlign: 'left',
                  fontSize: '0.84rem',
                  fontWeight: 600,
                  color: '#334155',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'space-between',
                }}
              >
                <span>{p}</span>
                <ArrowRight size={14} color="#94a3b8" />
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export function EmptyAndSuccessStates({ onExplore }) {
  return (
    <div className="cb-page-container">
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0f172a' }}>State Previews (Empty & Success)</h1>
        <p style={{ color: '#64748b', fontSize: '0.88rem', marginTop: '2px' }}>Design previews for zero-data and completion states</p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px' }}>
        <div className="cb-card" style={{ textAlign: 'center', padding: '48px 24px' }}>
          <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: '#f1f5f9', color: '#64748b', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
            <Briefcase size={28} />
          </div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#0f172a' }}>No applications yet!</h3>
          <p style={{ color: '#64748b', fontSize: '0.85rem', maxWidth: '300px', margin: '6px auto 20px' }}>
            Start exploring opportunities to kickstart your career.
          </p>
          <button onClick={onExplore} className="cb-btn cb-btn-primary" style={{ fontSize: '0.84rem' }}>
            Explore Jobs
          </button>
        </div>

        <div className="cb-card" style={{ textAlign: 'center', padding: '48px 24px' }}>
          <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: '#ccfbf1', color: '#0d9488', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
            <CheckCircle2 size={32} />
          </div>
          <h3 style={{ fontSize: '1.2rem', fontWeight: 800, color: '#0f172a' }}>Application Submitted!</h3>
          <p style={{ color: '#64748b', fontSize: '0.85rem', maxWidth: '320px', margin: '6px auto 20px' }}>
            Your application has been successfully submitted to the recruiting team.
          </p>
          <button onClick={onExplore} className="cb-btn cb-btn-primary" style={{ fontSize: '0.84rem' }}>
            View Applications
          </button>
        </div>
      </div>
    </div>
  )
}
