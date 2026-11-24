import { useState } from 'react'
import { Sparkles, FileText, CheckCircle2, Plus, ArrowRight, UserCheck } from 'lucide-react'
import { saveManualProfile } from '../services/resume'

const SUGGESTED_SKILLS = [
  'Python', 'React', 'JavaScript', 'TypeScript', 'FastAPI', 'Node.js',
  'PostgreSQL', 'Docker', 'Kubernetes', 'Data Structures & Algorithms',
  'Machine Learning', 'Git', 'AWS', 'Tailwind CSS', 'SQL'
]

function ManualProfileModal({ onClose, onProfileSaved }) {
  const [fullName, setFullName] = useState('')
  const [careerGoal, setCareerGoal] = useState('Full-Stack Developer')
  const [university, setUniversity] = useState('')
  const [graduationYear, setGraduationYear] = useState('2026')
  const [label, setLabel] = useState('Primary Profile')
  const [selectedSkills, setSelectedSkills] = useState(['Python', 'React', 'SQL'])
  const [customSkillInput, setCustomSkillInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  function toggleSkill(skill) {
    if (selectedSkills.includes(skill)) {
      setSelectedSkills(selectedSkills.filter((s) => s !== skill))
    } else {
      setSelectedSkills([...selectedSkills, skill])
    }
  }

  function handleAddCustomSkill(e) {
    e.preventDefault()
    const trimmed = customSkillInput.trim()
    if (trimmed && !selectedSkills.includes(trimmed)) {
      setSelectedSkills([...selectedSkills, trimmed])
      setCustomSkillInput('')
    }
  }

  async function handleSubmit(e) {
    e.preventDefault()
    if (!fullName.trim()) return setError('Please enter your full name')
    if (selectedSkills.length === 0) return setError('Please select at least 1 skill')

    setLoading(true)
    setError('')
    try {
      const res = await saveManualProfile({
        full_name: fullName,
        career_goal: careerGoal,
        target_role: careerGoal,
        university,
        graduation_year: graduationYear ? parseInt(graduationYear) : null,
        label,
        skills: selectedSkills,
      })
      if (onProfileSaved) {
        onProfileSaved(res.profile, res.resume)
      }
      onClose()
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Failed to save profile')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="modal-backdrop" style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      background: 'rgba(10, 15, 29, 0.75)',
      backdropFilter: 'blur(6px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '1rem',
    }}>
      <div className="modal-content" style={{
        background: '#131b2e',
        border: '1px solid #263554',
        borderRadius: '16px',
        width: '100%',
        maxWidth: '560px',
        maxHeight: '90vh',
        overflowY: 'auto',
        padding: '1.75rem',
        color: '#f8fafc',
        boxShadow: '0 20px 40px rgba(0,0,0,0.5)',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
          <div>
            <span style={{ fontSize: '0.75rem', textTransform: 'uppercase', color: '#818cf8', letterSpacing: '0.05em', fontWeight: 600 }}>
              Manual Onboarding
            </span>
            <h2 style={{ fontSize: '1.4rem', margin: '0.2rem 0 0 0', display: 'flex', alignItems: 'center', gap: '8px' }}>
              <UserCheck size={20} color="#6366f1" /> Create Profile Without PDF
            </h2>
          </div>
          <button onClick={onClose} style={{ background: 'transparent', border: 'none', color: '#94a3b8', fontSize: '1.4rem', cursor: 'pointer' }}>
            &times;
          </button>
        </div>

        {error && <div style={{ background: '#7f1d1d', color: '#fecaca', padding: '0.6rem 0.8rem', borderRadius: '8px', fontSize: '0.85rem', marginBottom: '1rem' }}>{error}</div>}

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.3rem' }}>Full Name *</label>
              <input
                type="text"
                required
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                placeholder="e.g. Rahul Sharma"
                style={{ width: '100%', padding: '0.6rem', background: '#0a0f1d', border: '1px solid #263554', borderRadius: '8px', color: '#fff', fontSize: '0.9rem' }}
              />
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.3rem' }}>Profile Label / Version</label>
              <input
                type="text"
                value={label}
                onChange={(e) => setLabel(e.target.value)}
                placeholder="e.g. Web Dev Resume"
                style={{ width: '100%', padding: '0.6rem', background: '#0a0f1d', border: '1px solid #263554', borderRadius: '8px', color: '#fff', fontSize: '0.9rem' }}
              />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.3rem' }}>Target Role / Goal</label>
              <select
                value={careerGoal}
                onChange={(e) => setCareerGoal(e.target.value)}
                style={{ width: '100%', padding: '0.6rem', background: '#0a0f1d', border: '1px solid #263554', borderRadius: '8px', color: '#fff', fontSize: '0.9rem' }}
              >
                <option value="Full-Stack Developer">Full-Stack Developer</option>
                <option value="Frontend Developer">Frontend Developer</option>
                <option value="Backend Developer">Backend Developer</option>
                <option value="AI/ML Engineer">AI/ML Engineer</option>
                <option value="Data Engineer">Data Engineer</option>
                <option value="DevOps / Cloud Engineer">DevOps / Cloud Engineer</option>
                <option value="Mobile App Developer">Mobile App Developer</option>
              </select>
            </div>
            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.3rem' }}>Graduation Year</label>
              <input
                type="number"
                value={graduationYear}
                onChange={(e) => setGraduationYear(e.target.value)}
                style={{ width: '100%', padding: '0.6rem', background: '#0a0f1d', border: '1px solid #263554', borderRadius: '8px', color: '#fff', fontSize: '0.9rem' }}
              />
            </div>
          </div>

          <div>
            <label style={{ display: 'block', fontSize: '0.8rem', color: '#94a3b8', marginBottom: '0.3rem' }}>College / University</label>
            <input
              type="text"
              value={university}
              onChange={(e) => setUniversity(e.target.value)}
              placeholder="e.g. National Institute of Technology"
              style={{ width: '100%', padding: '0.6rem', background: '#0a0f1d', border: '1px solid #263554', borderRadius: '8px', color: '#fff', fontSize: '0.9rem' }}
            />
          </div>

          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
              <label style={{ fontSize: '0.8rem', color: '#94a3b8' }}>Select Your Key Skills ({selectedSkills.length} selected)</label>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', maxHeight: '130px', overflowY: 'auto', padding: '4px' }}>
              {SUGGESTED_SKILLS.map((skill) => {
                const isSelected = selectedSkills.includes(skill)
                return (
                  <button
                    type="button"
                    key={skill}
                    onClick={() => toggleSkill(skill)}
                    style={{
                      padding: '4px 10px',
                      borderRadius: '999px',
                      fontSize: '0.78rem',
                      border: isSelected ? '1px solid #6366f1' : '1px solid #263554',
                      background: isSelected ? 'rgba(99, 102, 241, 0.25)' : '#0a0f1d',
                      color: isSelected ? '#a5b4fc' : '#94a3b8',
                      cursor: 'pointer',
                      transition: 'all 0.15s ease',
                    }}
                  >
                    {isSelected ? '✓ ' : '+ '} {skill}
                  </button>
                )
              })}
            </div>
          </div>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input
              type="text"
              value={customSkillInput}
              onChange={(e) => setCustomSkillInput(e.target.value)}
              placeholder="Add another skill (e.g. Django, GraphQL)..."
              style={{ flex: 1, padding: '0.5rem 0.75rem', background: '#0a0f1d', border: '1px solid #263554', borderRadius: '8px', color: '#fff', fontSize: '0.85rem' }}
              onKeyDown={(e) => { if (e.key === 'Enter') { handleAddCustomSkill(e) } }}
            />
            <button
              type="button"
              onClick={handleAddCustomSkill}
              style={{ padding: '0.5rem 0.9rem', background: '#263554', border: 'none', borderRadius: '8px', color: '#e2e8f0', cursor: 'pointer', fontSize: '0.85rem' }}
            >
              Add
            </button>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '0.5rem' }}>
            <button
              type="button"
              onClick={onClose}
              style={{ padding: '0.6rem 1.1rem', background: 'transparent', border: '1px solid #334155', borderRadius: '8px', color: '#94a3b8', cursor: 'pointer' }}
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '0.6rem 1.3rem',
                background: 'linear-gradient(135deg, #6366f1, #8b5cf6)',
                border: 'none',
                borderRadius: '8px',
                color: '#fff',
                fontWeight: 600,
                cursor: loading ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
              }}
            >
              {loading ? 'Saving...' : 'Save & Match Jobs →'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}

export default ManualProfileModal
