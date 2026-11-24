import { useState, useEffect } from 'react'
import { FileText, CheckCircle2, Plus, Sparkles, Layers, ArrowRight } from 'lucide-react'
import { getStudentResumes, activateResume } from '../services/resume'

function ResumeHub({ onResumeSwitched, onOpenManualModal, onOpenUploadModal }) {
  const [resumes, setResumes] = useState([])
  const [loading, setLoading] = useState(true)
  const [switchingId, setSwitchingId] = useState(null)

  async function loadResumes() {
    setLoading(true)
    try {
      const data = await getStudentResumes()
      setResumes(data || [])
    } catch (err) {
      console.error('Failed to load resumes:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadResumes()
  }, [])

  async function handleSwitch(resumeId) {
    setSwitchingId(resumeId)
    try {
      const res = await activateResume(resumeId)
      await loadResumes()
      if (onResumeSwitched) {
        onResumeSwitched(res.active_resume)
      }
    } catch (err) {
      console.error('Failed to switch resume:', err)
    } finally {
      setSwitchingId(null)
    }
  }

  return (
    <div className="resume-hub-card" style={{
      background: 'linear-gradient(180deg, #131b2e 0%, #0d1322 100%)',
      border: '1px solid #263554',
      borderRadius: '16px',
      padding: '1.5rem',
      marginBottom: '1.5rem',
      boxShadow: '0 8px 24px rgba(0,0,0,0.25)',
    }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem', marginBottom: '1.25rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span style={{ display: 'inline-flex', padding: '4px 8px', borderRadius: '6px', background: 'rgba(99,102,241,0.15)', color: '#818cf8', fontSize: '0.75rem', fontWeight: 600 }}>
              <Layers size={13} style={{ marginRight: '4px' }} /> MULTI-RESUME HUB
            </span>
          </div>
          <h3 style={{ fontSize: '1.3rem', margin: '0.4rem 0 0.2rem 0', color: '#f8fafc' }}>
            Target Different Roles with Dedicated Profiles
          </h3>
          <p style={{ margin: 0, fontSize: '0.85rem', color: '#94a3b8' }}>
            Switch your active profile to re-target your match feed between Web Dev, AI/ML, or DevOps.
          </p>
        </div>

        <div style={{ display: 'flex', gap: '0.6rem' }}>
          <button
            type="button"
            onClick={onOpenManualModal}
            style={{
              padding: '0.5rem 0.9rem',
              background: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '8px',
              color: '#cbd5e1',
              fontSize: '0.82rem',
              fontWeight: 500,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <Plus size={14} /> Add Profile Manually
          </button>
        </div>
      </div>

      {loading ? (
        <p style={{ color: '#64748b', fontSize: '0.85rem' }}>Loading saved resumes...</p>
      ) : resumes.length === 0 ? (
        <div style={{
          background: '#0a0f1d',
          border: '1px dashed #263554',
          borderRadius: '12px',
          padding: '1.25rem',
          textAlign: 'center',
          color: '#94a3b8',
        }}>
          <p style={{ margin: '0 0 0.75rem 0', fontSize: '0.9rem' }}>
            No saved resumes yet. Upload a PDF or quickly create one manually!
          </p>
          <div style={{ display: 'flex', justifyContent: 'center', gap: '0.75rem' }}>
            <button
              onClick={onOpenManualModal}
              style={{ padding: '0.45rem 0.9rem', background: '#6366f1', color: '#fff', border: 'none', borderRadius: '6px', fontSize: '0.82rem', cursor: 'pointer' }}
            >
              Fill Details Manually (1 min)
            </button>
          </div>
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: '0.75rem' }}>
          {resumes.map((r) => {
            const isActive = r.is_active
            const profile = r.parsed_profile || {}
            const skills = profile.skills || []

            return (
              <div
                key={r.id}
                style={{
                  background: isActive ? 'rgba(99, 102, 241, 0.08)' : '#0a0f1d',
                  border: isActive ? '1.5px solid #6366f1' : '1px solid #1e293b',
                  borderRadius: '12px',
                  padding: '1rem',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  transition: 'all 0.2s ease',
                }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.4rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                      <FileText size={16} color={isActive ? '#818cf8' : '#64748b'} />
                      <strong style={{ fontSize: '0.92rem', color: '#f8fafc' }}>{r.label}</strong>
                    </div>
                    {isActive && (
                      <span style={{ display: 'inline-flex', alignItems: 'center', gap: '4px', background: '#10b981', color: '#064e3b', fontSize: '0.68rem', fontWeight: 700, padding: '2px 6px', borderRadius: '999px' }}>
                        <CheckCircle2 size={10} /> ACTIVE
                      </span>
                    )}
                  </div>

                  <p style={{ margin: '0 0 0.5rem 0', fontSize: '0.78rem', color: '#818cf8', fontWeight: 500 }}>
                    {r.target_role || profile.career_goal || 'General Track'}
                  </p>

                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px', marginBottom: '0.75rem' }}>
                    {skills.slice(0, 4).map((s, idx) => (
                      <span key={idx} style={{ background: '#1e293b', color: '#94a3b8', fontSize: '0.72rem', padding: '2px 6px', borderRadius: '4px' }}>
                        {s.name || s}
                      </span>
                    ))}
                    {skills.length > 4 && (
                      <span style={{ fontSize: '0.7rem', color: '#64748b' }}>+{skills.length - 4} more</span>
                    )}
                  </div>
                </div>

                <div>
                  {isActive ? (
                    <div style={{ fontSize: '0.75rem', color: '#10b981', fontWeight: 500, padding: '0.35rem 0' }}>
                      Currently powering your job feed
                    </div>
                  ) : (
                    <button
                      type="button"
                      disabled={switchingId === r.id}
                      onClick={() => handleSwitch(r.id)}
                      style={{
                        width: '100%',
                        padding: '0.45rem',
                        background: '#1e293b',
                        border: '1px solid #334155',
                        borderRadius: '6px',
                        color: '#f8fafc',
                        fontSize: '0.78rem',
                        fontWeight: 600,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        gap: '4px',
                      }}
                    >
                      {switchingId === r.id ? 'Switching...' : 'Switch to this Profile →'}
                    </button>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default ResumeHub
