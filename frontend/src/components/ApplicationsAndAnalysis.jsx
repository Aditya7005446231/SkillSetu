import { useEffect, useState } from 'react'
import { getLearningRoadmap, saveLearningProgress } from '../services/opportunities'

const skillProgressKey = (skillName) => skillName.trim().toLowerCase()

export function MyApplicationsPage({ onExploreMore }) {
  const [activeTab, setActiveTab] = useState('All')

  const applications = [
    {
      id: 'app-1',
      title: 'SDE Intern',
      company: 'Microsoft',
      stage: 'Applied',
      date: 'Applied 2 days ago',
      logo: 'M',
      color: '#00a4ef',
    },
    {
      id: 'app-2',
      title: 'Data Analyst Intern',
      company: 'Deloitte',
      stage: 'Applied',
      date: 'Applied 4 days ago',
      logo: 'D',
      color: '#86bc25',
    },
    {
      id: 'app-3',
      title: 'SDE Intern',
      company: 'Amazon',
      stage: 'Applied',
      date: 'Applied 1 week ago',
      logo: 'A',
      color: '#ff9900',
    },
    {
      id: 'app-4',
      title: 'Product Intern',
      company: 'Google',
      stage: 'Shortlisted',
      date: 'Shortlisted 4 days ago',
      logo: 'G',
      color: '#4285f4',
    },
    {
      id: 'app-5',
      title: 'SDE Intern',
      company: 'Meta',
      stage: 'Shortlisted',
      date: 'Shortlisted 3 days ago',
      logo: 'M',
      color: '#0668e1',
    },
    {
      id: 'app-6',
      title: 'SDE Intern',
      company: 'Adobe',
      stage: 'Interview',
      date: 'Interview scheduled',
      logo: 'A',
      color: '#ed1c24',
    },
    {
      id: 'app-7',
      title: 'Systems Engineer',
      company: 'TCS',
      stage: 'Rejected',
      date: '2 weeks ago',
      logo: 'T',
      color: '#000000',
    },
  ]

  const stages = [
    { name: 'Applied', count: 3, color: '#2563eb', bg: '#eff6ff' },
    { name: 'Shortlisted', count: 2, color: '#f59e0b', bg: '#fffbeb' },
    { name: 'Interview', count: 1, color: '#10b981', bg: '#ecfdf5' },
    { name: 'Rejected', count: 1, color: '#f43f5e', bg: '#fff1f2' },
  ]

  return (
    <div className="cb-page-container">
      {/* Header with Title and Status Tabs */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0f172a' }}>My Applications</h1>
          <p style={{ color: '#64748b', fontSize: '0.88rem', marginTop: '2px' }}>Track your active job and internship applications</p>
        </div>

        <button
          onClick={onExploreMore}
          className="cb-btn cb-btn-primary"
          style={{ fontSize: '0.85rem' }}
        >
          Explore More Jobs
        </button>
      </div>

      {/* Demo Data Notice Banner */}
      <div style={{ padding: '10px 14px', background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: '8px', color: '#1e40af', fontSize: '0.82rem', marginBottom: '20px' }}>
        <strong>Demo Data:</strong> The application cards below are mock sample records for interface preview. Real backend application submission tracking is pending integration.
      </div>

      {/* Kanban / Multi-Column Stage Tracker */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '16px' }}>
        {stages.map((st) => {
          const list = applications.filter((a) => a.stage === st.name)
          return (
            <div key={st.name} style={{ background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '14px', padding: '16px', minHeight: '400px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '14px' }}>
                <span style={{ fontWeight: 700, fontSize: '0.9rem', color: '#0f172a' }}>
                  {st.name} ({list.length})
                </span>
                <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: st.color }} />
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
                {list.map((app) => (
                  <div
                    key={app.id}
                    style={{
                      background: '#fff',
                      border: '1px solid #e2e8f0',
                      borderRadius: '10px',
                      padding: '14px',
                      boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                    }}
                  >
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                      <div style={{ width: '28px', height: '28px', borderRadius: '6px', background: '#f1f5f9', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '0.8rem', color: app.color }}>
                        {app.logo}
                      </div>
                      <div>
                        <div style={{ fontSize: '0.88rem', fontWeight: 700, color: '#0f172a' }}>{app.company}</div>
                        <div style={{ fontSize: '0.78rem', color: '#64748b' }}>{app.title}</div>
                      </div>
                    </div>
                    <div style={{ fontSize: '0.72rem', color: '#94a3b8' }}>{app.date}</div>
                  </div>
                ))}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}

export function SkillAnalysisPage() {
  const skillsData = [
    { name: 'Python', level: 'Strong', percent: 90, barColor: '#10b981' },
    { name: 'SQL & Databases', level: 'Strong', percent: 85, barColor: '#10b981' },
    { name: 'React & Frontend', level: 'Intermediate', percent: 75, barColor: '#2563eb' },
    { name: 'Data Structures & Algorithms', level: 'Intermediate', percent: 68, barColor: '#2563eb' },
    { name: 'Docker & Microservices', level: 'Needs Improvement', percent: 45, barColor: '#f59e0b' },
    { name: 'System Design', level: 'Needs Improvement', percent: 40, barColor: '#f43f5e' },
  ]

  return (
    <div className="cb-page-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <div>
          <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0f172a' }}>Your Skills Overview</h1>
          <p style={{ color: '#64748b', fontSize: '0.88rem', marginTop: '2px' }}>Track your skill proficiencies and discover targeted areas for improvement.</p>
        </div>
        <button className="cb-btn cb-btn-secondary" style={{ fontSize: '0.84rem' }}>
          View Detailed Framework Analysis →
        </button>
      </div>

      {/* Simulated Data Disclaimer */}
      <div style={{ padding: '10px 14px', background: '#eff6ff', border: '1px solid #bfdbfe', borderRadius: '8px', color: '#1e40af', fontSize: '0.82rem', marginBottom: '20px' }}>
        <strong>Simulated Data:</strong> This overall score and proficiency breakdown are simulated sample data for preview purposes. Your verified skills from CV analysis appear in Overview and Profile.
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.8fr', gap: '22px' }}>
        {/* Overall Score Radial Card */}
        <div className="cb-card" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', textAlign: 'center', padding: '36px 20px' }}>
          <div style={{
            width: '140px',
            height: '140px',
            borderRadius: '50%',
            background: 'conic-gradient(#0d9488 0% 76%, #e2e8f0 76% 100%)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            marginBottom: '20px',
          }}>
            <div style={{
              width: '110px',
              height: '110px',
              borderRadius: '50%',
              background: '#fff',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              <span style={{ fontSize: '1.8rem', fontWeight: 800, color: '#0f172a' }}>76%</span>
              <span style={{ fontSize: '0.72rem', color: '#64748b', fontWeight: 600 }}>Overall Score</span>
            </div>
          </div>

          <div style={{ display: 'flex', gap: '16px', marginTop: '10px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}>
              <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#10b981' }} />
              <span>Strong (5)</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}>
              <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#2563eb' }} />
              <span>Intermediate (3)</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', fontSize: '0.8rem' }}>
              <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: '#f59e0b' }} />
              <span>Needs Boost (2)</span>
            </div>
          </div>
        </div>

        {/* Top Skills Breakdown Bars */}
        <div className="cb-card">
          <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#0f172a', marginBottom: '18px' }}>Top Skills Proficiency</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {skillsData.map((s, idx) => (
              <div key={idx}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                  <span style={{ fontSize: '0.86rem', fontWeight: 600, color: '#0f172a' }}>{s.name}</span>
                  <span style={{ fontSize: '0.82rem', fontWeight: 700, color: s.barColor }}>{s.percent}%</span>
                </div>
                <div style={{ width: '100%', height: '8px', background: '#f1f5f9', borderRadius: '999px', overflow: 'hidden' }}>
                  <div style={{ width: `${s.percent}%`, height: '100%', background: s.barColor, borderRadius: '999px' }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export function LearningRoadmapPage() {
  const [roadmaps, setRoadmaps] = useState(null)
  const [selectedJobId, setSelectedJobId] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [reloadKey, setReloadKey] = useState(0)
  const [progressBySkill, setProgressBySkill] = useState({})
  const [progressDrafts, setProgressDrafts] = useState({})
  const [savingBySkill, setSavingBySkill] = useState({})
  const [progressErrors, setProgressErrors] = useState({})

  useEffect(() => {
    let active = true

    getLearningRoadmap()
      .then((result) => {
        if (active) {
          setRoadmaps(result)
          setSelectedJobId((current) => current || result.target_roadmaps?.[0]?.job_id || '')
          const progress = result.progress || []
          setProgressBySkill(Object.fromEntries(
            progress.map((item) => [skillProgressKey(item.skill_name), item]),
          ))
          setProgressDrafts(Object.fromEntries(
            progress.map((item) => [
              skillProgressKey(item.skill_name),
              {
                status: item.status,
                evidence_url: item.evidence_url || '',
                evidence_note: item.evidence_note || '',
              },
            ]),
          ))
        }
      })
      .catch((requestError) => {
        if (active) {
          console.error('Unable to load learning roadmap:', requestError)
          setError(requestError.response?.data?.detail || requestError.message || 'Unable to load your roadmap.')
        }
      })
      .finally(() => {
        if (active) setLoading(false)
      })

    return () => {
      active = false
    }
  }, [reloadKey])

  const availableJobs = roadmaps?.available_jobs || []
  const targetRoadmaps = roadmaps?.target_roadmaps || []
  const targetRoadmap = targetRoadmaps.find((item) => item.job_id === selectedJobId) || targetRoadmaps[0]
  const sharedCore = roadmaps?.shared_core

  const updateProgressDraft = (skillName, field, value) => {
    const key = skillProgressKey(skillName)
    setProgressDrafts((current) => ({
      ...current,
      [key]: {
        status: current[key]?.status || progressBySkill[key]?.status || 'not_started',
        evidence_url: current[key]?.evidence_url || progressBySkill[key]?.evidence_url || '',
        evidence_note: current[key]?.evidence_note || progressBySkill[key]?.evidence_note || '',
        ...current[key],
        [field]: value,
      },
    }))
    setProgressErrors((current) => ({ ...current, [key]: '' }))
  }

  const saveProgress = async (skillName) => {
    const key = skillProgressKey(skillName)
    const saved = progressBySkill[key]
    const draft = progressDrafts[key] || {
      status: saved?.status || 'not_started',
      evidence_url: saved?.evidence_url || '',
      evidence_note: saved?.evidence_note || '',
    }

    if (
      draft.status === 'completed'
      && !draft.evidence_url.trim()
      && draft.evidence_note.trim().length < 20
    ) {
      setProgressErrors((current) => ({
        ...current,
        [key]: 'Add a project URL or at least 20 characters describing your evidence.',
      }))
      return
    }

    setSavingBySkill((current) => ({ ...current, [key]: true }))
    setProgressErrors((current) => ({ ...current, [key]: '' }))
    try {
      const updated = await saveLearningProgress({
        skill_name: skillName,
        status: draft.status,
        evidence_url: draft.evidence_url.trim() || null,
        evidence_note: draft.evidence_note.trim(),
      })
      const updatedKey = skillProgressKey(updated.skill_name)
      setProgressBySkill((current) => ({ ...current, [updatedKey]: updated }))
      setProgressDrafts((current) => ({
        ...current,
        [updatedKey]: {
          status: updated.status,
          evidence_url: updated.evidence_url || '',
          evidence_note: updated.evidence_note || '',
        },
      }))
    } catch (requestError) {
      const detail = requestError.response?.data?.detail
      const message = Array.isArray(detail)
        ? detail.map((item) => item.msg).join(' ')
        : (detail || requestError.message || 'Unable to save progress.')
      setProgressErrors((current) => ({ ...current, [key]: message }))
    } finally {
      setSavingBySkill((current) => ({ ...current, [key]: false }))
    }
  }

  const visibleSkills = [
    ...(targetRoadmap?.steps || []).map((step) => step.skill),
    ...(sharedCore?.steps || []).map((step) => step.skill),
  ]
  const uniqueVisibleSkills = [...new Set(visibleSkills.map(skillProgressKey))]
  const completedSkills = uniqueVisibleSkills.filter(
    (key) => progressBySkill[key]?.status === 'completed',
  ).length

  const renderSteps = (steps) => (
    steps.length ? (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        {steps.map((step) => {
          const key = skillProgressKey(step.skill)
          const saved = progressBySkill[key]
          const draft = progressDrafts[key] || {
            status: saved?.status || 'not_started',
            evidence_url: saved?.evidence_url || '',
            evidence_note: saved?.evidence_note || '',
          }

          return (
            <div
              key={`${step.order}-${step.skill}`}
              style={{ border: '1px solid #e2e8f0', borderRadius: '10px', padding: '14px' }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', gap: '12px', alignItems: 'center', flexWrap: 'wrap' }}>
                <strong style={{ color: '#0f172a' }}>{step.order}. {step.skill}</strong>
                <span style={{
                  color: step.kind === 'prerequisite' ? '#92400e' : '#0f766e',
                  background: step.kind === 'prerequisite' ? '#fef3c7' : '#ccfbf1',
                  borderRadius: '999px',
                  padding: '3px 9px',
                  fontSize: '0.72rem',
                  fontWeight: 700,
                }}>
                  {step.kind === 'prerequisite' ? 'Prerequisite' : 'Job requirement'}
                </span>
              </div>
              {step.description && <p style={{ color: '#475569', fontSize: '0.83rem', margin: '8px 0 4px' }}>{step.description}</p>}
              <p style={{ color: '#64748b', fontSize: '0.82rem', margin: '8px 0 4px' }}>{step.reason}</p>
              <p style={{ color: '#0f172a', fontSize: '0.84rem', fontWeight: 650, margin: '10px 0 5px' }}>Task: {step.learning_task}</p>
              <ul style={{ color: '#64748b', fontSize: '0.8rem', margin: '4px 0 12px', paddingLeft: '20px' }}>
                {step.acceptance_criteria.map((criterion) => <li key={criterion}>{criterion}</li>)}
              </ul>

              <div style={{ display: 'grid', gridTemplateColumns: 'minmax(150px, 0.7fr) minmax(180px, 1fr)', gap: '8px', marginTop: '12px' }}>
                <label style={{ display: 'flex', flexDirection: 'column', gap: '4px', color: '#475569', fontSize: '0.76rem', fontWeight: 600 }}>
                  Progress
                  <select
                    value={draft.status}
                    onChange={(event) => updateProgressDraft(step.skill, 'status', event.target.value)}
                    style={{ padding: '8px', border: '1px solid #cbd5e1', borderRadius: '7px', background: '#fff', color: '#0f172a' }}
                  >
                    <option value="not_started">Not started</option>
                    <option value="in_progress">In progress</option>
                    <option value="completed">Evidence submitted</option>
                  </select>
                </label>
                <label style={{ display: 'flex', flexDirection: 'column', gap: '4px', color: '#475569', fontSize: '0.76rem', fontWeight: 600 }}>
                  Project URL
                  <input
                    type="url"
                    value={draft.evidence_url}
                    onChange={(event) => updateProgressDraft(step.skill, 'evidence_url', event.target.value)}
                    placeholder="https://github.com/..."
                    style={{ padding: '8px', border: '1px solid #cbd5e1', borderRadius: '7px', color: '#0f172a' }}
                  />
                </label>
              </div>
              <label style={{ display: 'flex', flexDirection: 'column', gap: '4px', color: '#475569', fontSize: '0.76rem', fontWeight: 600, marginTop: '8px' }}>
                Evidence note
                <textarea
                  value={draft.evidence_note}
                  onChange={(event) => updateProgressDraft(step.skill, 'evidence_note', event.target.value)}
                  placeholder="What did you build or practice? Required to submit completion without a project URL."
                  rows={2}
                  maxLength={2000}
                  style={{ padding: '8px', border: '1px solid #cbd5e1', borderRadius: '7px', color: '#0f172a', resize: 'vertical' }}
                />
              </label>
              <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap', marginTop: '9px' }}>
                <button
                  className="cb-btn cb-btn-secondary"
                  disabled={Boolean(savingBySkill[key])}
                  onClick={() => saveProgress(step.skill)}
                >
                  {savingBySkill[key] ? 'Saving…' : 'Save progress'}
                </button>
                {saved?.status === 'completed' && (
                  <span style={{ color: '#64748b', fontSize: '0.74rem' }}>Evidence submitted; not automatically verified.</span>
                )}
                {saved?.evidence_url && (
                  <a
                    href={saved.evidence_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    style={{ fontSize: '0.78rem', color: '#0f766e' }}
                  >
                    Open submitted project
                  </a>
                )}
              </div>
              {progressErrors[key] && <p role="alert" style={{ color: '#b91c1c', fontSize: '0.78rem', marginBottom: 0 }}>{progressErrors[key]}</p>}
            </div>
          )
        })}
      </div>
    ) : (
      <p style={{ color: '#64748b', margin: 0 }}>No missing required skills were found for this roadmap.</p>
    )
  )

  return (
    <div className="cb-page-container">
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.6rem', fontWeight: 800, color: '#0f172a' }}>Your Learning Roadmap</h1>
        <p style={{ color: '#64748b', fontSize: '0.88rem', marginTop: '2px' }}>
          Focused on job requirements, your active profile, and explicit framework prerequisites.
        </p>
      </div>

      {loading ? (
        <div className="cb-card" role="status">Building your roadmap from current recommendations…</div>
      ) : error ? (
        <div className="cb-card" role="alert" style={{ color: '#b91c1c' }}>
          <p>{error}</p>
          <button
            className="cb-btn cb-btn-secondary"
            onClick={() => {
              setLoading(true)
              setError('')
              setReloadKey((key) => key + 1)
            }}
          >
            Try again
          </button>
        </div>
      ) : availableJobs.length === 0 ? (
        <div className="cb-card" role="status">
          <h3 style={{ marginTop: 0 }}>No evidence-based roadmap yet</h3>
          <p style={{ color: '#64748b', marginBottom: 0 }}>
            Add skills to your active profile and ensure there are active jobs with extracted skill requirements.
            We won’t invent gaps when matching data is unavailable.
          </p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '22px' }}>
          <div className="cb-card" role="status">
            <strong>Roadmap progress: {completedSkills} of {uniqueVisibleSkills.length} skills have evidence submitted.</strong>
            <p style={{ color: '#64748b', fontSize: '0.78rem', margin: '5px 0 0' }}>
              Submitting evidence tracks your progress; it does not automatically verify the skill or change your job match score.
            </p>
          </div>
          <div className="cb-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: '16px', flexWrap: 'wrap', marginBottom: '18px' }}>
              <div>
                <h2 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#0f172a', margin: 0 }}>Roadmap for a target job</h2>
                <p style={{ color: '#64748b', fontSize: '0.82rem', margin: '5px 0 0' }}>
                  Steps only include that job’s missing requirements and their listed prerequisites.
                </p>
              </div>
              <label style={{ display: 'flex', flexDirection: 'column', gap: '5px', minWidth: '240px', color: '#475569', fontSize: '0.8rem', fontWeight: 600 }}>
                Choose a target job
                <select
                  value={targetRoadmap?.job_id || ''}
                  onChange={(event) => setSelectedJobId(event.target.value)}
                  style={{ padding: '9px 10px', border: '1px solid #cbd5e1', borderRadius: '8px', background: '#fff', color: '#0f172a' }}
                >
                  {targetRoadmaps.map((job) => (
                    <option key={job.job_id} value={job.job_id}>
                      {job.title}{job.company ? ` — ${job.company}` : ''}{job.location ? ` (${job.location})` : ''}
                    </option>
                  ))}
                </select>
              </label>
            </div>

            {targetRoadmap && (
              <>
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', flexWrap: 'wrap', marginBottom: '14px' }}>
                  <strong style={{ color: '#0f172a' }}>{targetRoadmap.title}</strong>
                  {targetRoadmap.company && <span style={{ color: '#64748b' }}>at {targetRoadmap.company}</span>}
                  {targetRoadmap.location && <span style={{ color: '#64748b' }}>{targetRoadmap.location}</span>}
                  <span style={{ color: '#0f766e', background: '#ccfbf1', borderRadius: '999px', padding: '3px 9px', fontSize: '0.75rem', fontWeight: 700 }}>
                    Match {targetRoadmap.match_score}%
                  </span>
                </div>
                {targetRoadmap.missing_skills.length > 0 && (
                  <p style={{ color: '#475569', fontSize: '0.84rem' }}>
                    Requirements not found in your active profile: <strong>{targetRoadmap.missing_skills.join(', ')}</strong>
                  </p>
                )}
                {renderSteps(targetRoadmap.steps)}
                {targetRoadmap.project && (
                  <div style={{ marginTop: '16px', padding: '13px', borderRadius: '9px', background: '#f0fdfa', color: '#115e59', fontSize: '0.85rem' }}>
                    <strong>Proof of learning:</strong> {targetRoadmap.project}
                  </div>
                )}
              </>
            )}
          </div>

          <div className="cb-card">
            <h2 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#0f172a', margin: '0 0 5px' }}>Shared core across top matches</h2>
            <p style={{ color: '#64748b', fontSize: '0.82rem', marginTop: 0, marginBottom: '16px' }}>
              Only skills missing from at least two of the top {sharedCore?.source_job_count || 0} matched roles appear here.
            </p>
            {sharedCore?.skills?.length ? (
              <>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '16px' }}>
                  {sharedCore.skills.map((skill) => (
                    <div key={skill.name} style={{ border: '1px solid #e2e8f0', borderRadius: '9px', padding: '11px' }}>
                      <strong style={{ color: '#0f172a' }}>{skill.name}</strong>
                      <span style={{ color: '#64748b', fontSize: '0.8rem' }}> — missing in {skill.occurrences}/{sharedCore.source_job_count} roles</span>
                      <div style={{ color: '#64748b', fontSize: '0.77rem', marginTop: '4px' }}>Roles: {skill.roles.join(', ')}</div>
                    </div>
                  ))}
                </div>
                {renderSteps(sharedCore.steps)}
                {sharedCore.project && (
                  <div style={{ marginTop: '16px', padding: '13px', borderRadius: '9px', background: '#f0fdfa', color: '#115e59', fontSize: '0.85rem' }}>
                    <strong>Shared proof project:</strong> {sharedCore.project}
                  </div>
                )}
              </>
            ) : (
              <p style={{ color: '#64748b', margin: 0 }}>{sharedCore?.message || 'No repeated skill gaps found.'}</p>
            )}
          </div>

          <p style={{ color: '#64748b', fontSize: '0.78rem', margin: 0 }}>
            “Missing” means the skill was not found in the active resume profile; it may not reflect everything you can do. Update your profile if a skill was overlooked.
          </p>
        </div>
      )}
    </div>
  )
}
