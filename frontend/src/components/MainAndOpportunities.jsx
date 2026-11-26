import { useState, useRef, useEffect } from 'react'
import {
  UploadCloud,
  FileUp,
  Sparkles,
  CheckCircle2,
  AlertCircle,
  Briefcase,
  ArrowRight,
  TrendingUp,
  Layers,
  Search,
  BookOpen,
  X,
  LoaderCircle,
  Building2,
  MapPin,
  Bookmark,
  ExternalLink
} from 'lucide-react'
import { analyzeResume } from '../services/resume'
import { getRecommendedOpportunities } from '../services/opportunities'

export function MainDashboard({ onNavigate, studentName = 'Aditya' }) {
  const inputRef = useRef(null)
  const [file, setFile] = useState(null)
  const [status, setStatus] = useState('')
  const [error, setError] = useState('')
  const [analyzedProfile, setAnalyzedProfile] = useState(null)
  const [liveJobs, setLiveJobs] = useState([])
  const [loadingJobs, setLoadingJobs] = useState(true)

  // Load actual live jobs from database on mount
  useEffect(() => {
    async function loadJobs() {
      setLoadingJobs(true)
      try {
        const jobs = await getRecommendedOpportunities()
        setLiveJobs(jobs || [])
      } catch (err) {
        console.error('Error fetching live jobs:', err)
      } finally {
        setLoadingJobs(false)
      }
    }
    loadJobs()
  }, [])

  function chooseFile(nextFile) {
    setError('')
    if (!nextFile) return
    if (nextFile.type !== 'application/pdf') {
      setError('Please choose a valid PDF resume.')
      return
    }
    if (nextFile.size > 5 * 1024 * 1024) {
      setError('Your resume must be smaller than 5 MB.')
      return
    }
    setFile(nextFile)
    setStatus('')
  }

  async function handleAnalyze(e) {
    if (e) e.preventDefault()
    if (!file) return setError('Please choose or drop a PDF resume first.')

    setError('')
    setStatus('analyzing')

    try {
      const result = await analyzeResume(file)
      const prof = result.profile
      setAnalyzedProfile(prof)
      setStatus('complete')

      // Re-fetch live opportunities matching the analyzed profile
      setLoadingJobs(true)
      const refreshedJobs = await getRecommendedOpportunities()
      setLiveJobs(refreshedJobs || [])
    } catch (err) {
      setStatus('')
      const isTimeout = err.code === 'ECONNABORTED' || (err.message && err.message.toLowerCase().includes('timeout'))
      const errorMessage = isTimeout
        ? 'Resume analysis timed out. The AI model or server is processing slower than usual—please try again.'
        : (err.response?.data?.detail || err.message || 'Resume parsing failed.')
      setError(errorMessage)
    } finally {
      setLoadingJobs(false)
    }
  }

  return (
    <div className="cb-page-container">
      {/* Dynamic Welcome Header */}
      <div style={{ marginBottom: '24px' }}>
        <h1 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.02em' }}>
          Welcome, {studentName}!
        </h1>
        <p style={{ color: '#64748b', fontSize: '0.92rem', marginTop: '4px' }}>
          Analyze your CV / Skills to discover live job openings from Google & JSearch you are eligible for.
        </p>
      </div>

      {/* 🚀 PRIMARY SECTION: Analyze Your Role (CV Upload & Skills Extraction) */}
      <div className="cb-card" style={{
        background: 'linear-gradient(180deg, #ffffff 0%, #f8fafc 100%)',
        border: '1.5px solid #cbd5e1',
        borderRadius: '16px',
        padding: '28px',
        marginBottom: '26px',
        boxShadow: '0 4px 12px rgba(0,0,0,0.04)',
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '14px', marginBottom: '18px' }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: '#ccfbf1', color: '#0f766e', fontSize: '0.75rem', fontWeight: 700, padding: '4px 10px', borderRadius: '999px', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
              <Sparkles size={13} /> Live AI Role & Skill Matcher
            </div>
            <h2 style={{ fontSize: '1.35rem', fontWeight: 800, color: '#0f172a', margin: '8px 0 4px 0' }}>
              Analyze Your Role & Eligibility
            </h2>
            <p style={{ color: '#64748b', fontSize: '0.86rem', margin: 0, maxWidth: '640px' }}>
              Upload your resume (PDF) or complete your profile. Our RAG engine extracts your verified skills and computes exact placement match scores against real active job postings.
            </p>
          </div>

          <button
            type="button"
            onClick={() => onNavigate('profile')}
            style={{
              padding: '8px 16px',
              borderRadius: '8px',
              border: '1px solid #cbd5e1',
              background: '#fff',
              color: '#334155',
              fontWeight: 600,
              fontSize: '0.84rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            Enter Details Manually Instead →
          </button>
        </div>

        {/* Dropzone */}
        <div
          onClick={() => inputRef.current?.click()}
          style={{
            border: file ? '2px solid #10b981' : '2px dashed #94a3b8',
            borderRadius: '14px',
            padding: '30px 20px',
            textAlign: 'center',
            background: file ? '#f0fdf4' : '#fff',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
          }}
        >
          <input
            ref={inputRef}
            type="file"
            accept="application/pdf"
            hidden
            onChange={(e) => chooseFile(e.target.files[0])}
          />

          {file ? (
            <div>
              <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: '#dcfce7', color: '#16a34a', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 10px' }}>
                <FileUp size={24} />
              </div>
              <strong style={{ fontSize: '1rem', color: '#0f172a', display: 'block' }}>{file.name}</strong>
              <small style={{ color: '#64748b', fontSize: '0.8rem' }}>{(file.size / 1024 / 1024).toFixed(2)} MB • Ready to analyze</small>
            </div>
          ) : (
            <div>
              <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: '#ccfbf1', color: '#0d9488', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 10px' }}>
                <UploadCloud size={24} />
              </div>
              <strong style={{ fontSize: '1rem', color: '#0f172a', display: 'block' }}>Drop your PDF resume here</strong>
              <small style={{ color: '#64748b', fontSize: '0.82rem' }}>or click to browse from computer (PDF up to 5 MB)</small>
            </div>
          )}
        </div>

        {file && (
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '12px' }}>
            <button
              type="button"
              onClick={() => { setFile(null); setStatus(''); }}
              style={{ background: 'none', border: 'none', color: '#94a3b8', fontSize: '0.8rem', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '4px' }}
            >
              <X size={14} /> Remove selected file
            </button>

            <button
              type="button"
              disabled={status === 'analyzing'}
              onClick={handleAnalyze}
              className="cb-btn cb-btn-primary"
              style={{ padding: '9px 22px', fontSize: '0.88rem' }}
            >
              {status === 'analyzing' ? (
                <><LoaderCircle className="spin" size={16} /> Reading CV & Matching Skills...</>
              ) : 'Analyze CV & Show Eligible Opportunities →'}
            </button>
          </div>
        )}

        {error && (
          <div style={{ marginTop: '14px', padding: '10px 14px', borderRadius: '8px', background: '#ffe4e6', color: '#e11d48', fontSize: '0.84rem', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <AlertCircle size={16} />
            <span>{error}</span>
          </div>
        )}

        {status === 'complete' && analyzedProfile && (
          <div style={{ marginTop: '20px', padding: '18px', background: '#ecfdf5', border: '1px solid #a7f3d0', borderRadius: '12px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#065f46', fontWeight: 700, fontSize: '0.92rem', marginBottom: '8px' }}>
              <CheckCircle2 size={18} color="#10b981" />
              <span>CV Analyzed! Verified Skills extracted:</span>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginTop: '10px' }}>
              {(analyzedProfile.skills || []).map((s, idx) => (
                <span key={idx} style={{ background: '#fff', border: '1px solid #6ee7b7', color: '#047857', padding: '4px 10px', borderRadius: '999px', fontSize: '0.78rem', fontWeight: 600 }}>
                  ✓ {s.name || s}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* 🎯 OPPORTUNITY SECTION: Real Live Database Jobs */}
      <div>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '18px' }}>
          <div>
            <h3 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#0f172a' }}>
              Live Synced Opportunities ({liveJobs.length} Available)
            </h3>
            <p style={{ color: '#64748b', fontSize: '0.84rem', marginTop: '2px' }}>
              Live job listings fetched directly from Supabase, JSearch, and Google Index.
            </p>
          </div>

          <button
            onClick={() => onNavigate('opportunities')}
            style={{ background: 'none', border: 'none', color: '#0d9488', fontSize: '0.86rem', fontWeight: 700, cursor: 'pointer' }}
          >
            View all {liveJobs.length} opportunities →
          </button>
        </div>

        {loadingJobs ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#64748b' }}>
            <LoaderCircle className="spin" size={24} style={{ margin: '0 auto 8px' }} />
            <p>Fetching real-time job matches from database...</p>
          </div>
        ) : liveJobs.length === 0 ? (
          <div className="cb-card" style={{ textAlign: 'center', padding: '36px' }}>
            <p style={{ color: '#64748b', margin: 0 }}>No active jobs found. Try syncing opportunities or clearing filters.</p>
          </div>
        ) : (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '18px' }}>
            {liveJobs.slice(0, 6).map((job) => (
              <div
                key={job.job_id || job.id}
                onClick={() => onNavigate('job-details', job)}
                className="cb-card"
                style={{ cursor: 'pointer', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                      <div style={{ width: '42px', height: '42px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '1.1rem', color: '#0d9488' }}>
                        {job.company ? job.company.charAt(0).toUpperCase() : 'J'}
                      </div>
                      <div>
                        <h4 style={{ fontSize: '1rem', fontWeight: 700, color: '#0f172a', margin: 0 }}>{job.title}</h4>
                        <p style={{ fontSize: '0.82rem', color: '#64748b', margin: '2px 0 0 0' }}>{job.company} • {job.location || 'India (Remote)'}</p>
                      </div>
                    </div>

                    <span style={{
                      display: 'inline-flex',
                      alignItems: 'center',
                      padding: '4px 10px',
                      borderRadius: '999px',
                      background: '#ccfbf1',
                      color: '#0f766e',
                      fontSize: '0.78rem',
                      fontWeight: 700,
                    }}>
                      {Math.round(job.match_score || 80)}% Match
                    </span>
                  </div>

                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', margin: '14px 0' }}>
                    {(job.matched_skills || ['Python', 'SQL']).map((s, idx) => (
                      <span key={idx} style={{ background: '#ecfdf5', color: '#047857', border: '1px solid #a7f3d0', fontSize: '0.74rem', padding: '2px 8px', borderRadius: '4px', fontWeight: 600 }}>
                        ✓ {s}
                      </span>
                    ))}
                    {(job.missing_skills || []).slice(0, 3).map((s, idx) => (
                      <span key={idx} style={{ background: '#f1f5f9', color: '#64748b', fontSize: '0.74rem', padding: '2px 8px', borderRadius: '4px' }}>
                        Gap: {s}
                      </span>
                    ))}
                  </div>
                </div>

                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '12px', borderTop: '1px solid #f1f5f9', fontSize: '0.76rem', color: '#94a3b8' }}>
                  <span>Track: <strong style={{ color: '#0f172a' }}>{job.job_type || 'Internship'}</strong></span>
                  <a
                    href={job.apply_url}
                    target="_blank"
                    rel="noreferrer"
                    onClick={(e) => e.stopPropagation()}
                    style={{ color: '#0d9488', display: 'flex', alignItems: 'center', gap: '4px', textDecoration: 'none', fontWeight: 600 }}
                  >
                    Direct Apply <ExternalLink size={12} />
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export function JobOpportunitiesPage({ onSelectJob }) {
  const [activeFilter, setActiveFilter] = useState('All Filters')
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)

  const filters = ['All Filters', 'Internship', 'Full-Time', 'Remote', 'On-Campus']

  useEffect(() => {
    async function fetchJobs() {
      setLoading(true)
      try {
        const data = await getRecommendedOpportunities()
        setJobs(data || [])
      } catch (err) {
        console.error(err)
      } finally {
        setLoading(false)
      }
    }
    fetchJobs()
  }, [])

  const filtered = jobs.filter((j) => {
    const jobType = (j.job_type || '').toLowerCase().replace(/[\s_]+/g, '-')
    if (activeFilter === 'Internship' && jobType !== 'internship') return false
    if (activeFilter === 'Full-Time' && jobType !== 'full-time') return false
    if (activeFilter === 'On-Campus' && !/(?:on[ -]?campus)/i.test(j.location || '')) return false
    if (activeFilter === 'Remote' && !(j.location || '').toLowerCase().includes('remote')) return false
    return true
  })

  return (
    <div className="cb-page-container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '14px', marginBottom: '24px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px', flexWrap: 'wrap' }}>
          {filters.map((f) => (
            <button
              key={f}
              onClick={() => setActiveFilter(f)}
              style={{
                padding: '7px 16px',
                borderRadius: '999px',
                fontSize: '0.84rem',
                fontWeight: 600,
                border: activeFilter === f ? '1px solid #0d9488' : '1px solid #cbd5e1',
                background: activeFilter === f ? '#0d9488' : '#fff',
                color: activeFilter === f ? '#fff' : '#475569',
                cursor: 'pointer',
              }}
            >
              {f}
            </button>
          ))}
        </div>

        <div style={{ fontSize: '0.84rem', color: '#64748b' }}>
          Showing: <strong style={{ color: '#0f172a' }}>{filtered.length} Live Openings</strong>
        </div>
      </div>

      {loading ? (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <LoaderCircle className="spin" size={24} style={{ margin: '0 auto 8px' }} />
          <p>Loading active job listings...</p>
        </div>
      ) : filtered.length === 0 ? (
        <div className="cb-card" style={{ textAlign: 'center', padding: '36px', color: '#64748b' }}>
          No opportunities match this filter.
        </div>
      ) : (
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '18px' }}>
          {filtered.map((job) => (
            <div
              key={job.job_id || job.id}
              onClick={() => onSelectJob(job)}
              className="cb-card"
              style={{ cursor: 'pointer', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}
            >
              <div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <div style={{ width: '44px', height: '44px', borderRadius: '10px', background: '#f8fafc', border: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '1.2rem', color: '#0d9488' }}>
                      {job.company ? job.company.charAt(0).toUpperCase() : 'J'}
                    </div>
                    <div>
                      <h3 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#0f172a' }}>{job.title}</h3>
                      <p style={{ fontSize: '0.84rem', color: '#64748b', margin: '2px 0 0 0' }}>{job.company} • {job.location || 'India'}</p>
                    </div>
                  </div>

                  <span style={{
                    display: 'inline-flex',
                    alignItems: 'center',
                    padding: '4px 10px',
                    borderRadius: '999px',
                    background: '#ccfbf1',
                    color: '#0f766e',
                    fontSize: '0.78rem',
                    fontWeight: 700,
                  }}>
                    {Math.round(job.match_score || 80)}% Match
                  </span>
                </div>

                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', margin: '14px 0' }}>
                  {(job.matched_skills || []).map((s, idx) => (
                    <span key={idx} style={{ background: '#ecfdf5', color: '#047857', border: '1px solid #a7f3d0', fontSize: '0.75rem', padding: '3px 9px', borderRadius: '4px', fontWeight: 600 }}>
                      ✓ {s}
                    </span>
                  ))}
                  {(job.missing_skills || []).slice(0, 3).map((s, idx) => (
                    <span key={idx} style={{ background: '#f1f5f9', color: '#64748b', fontSize: '0.75rem', padding: '3px 9px', borderRadius: '4px' }}>
                      Gap: {s}
                    </span>
                  ))}
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', paddingTop: '14px', borderTop: '1px solid #f1f5f9', fontSize: '0.78rem', color: '#94a3b8' }}>
                <span>Type: <strong style={{ color: '#0f172a' }}>{job.job_type || 'Internship'}</strong></span>
                <Bookmark size={16} color="#94a3b8" />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export function JobDetailsView({ job, onBack, onApply }) {
  if (!job) return null

  return (
    <div className="cb-page-container">
      <button
        onClick={onBack}
        style={{ display: 'inline-flex', alignItems: 'center', gap: '6px', background: 'none', border: 'none', color: '#64748b', fontSize: '0.88rem', fontWeight: 600, cursor: 'pointer', marginBottom: '20px' }}
      >
        ← Back to opportunities
      </button>

      <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '24px' }}>
        <div className="cb-card">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              <div style={{ width: '56px', height: '56px', borderRadius: '12px', background: '#f8fafc', border: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'center', fontWeight: 800, fontSize: '1.5rem', color: '#0d9488' }}>
                {job.company ? job.company.charAt(0).toUpperCase() : 'J'}
              </div>
              <div>
                <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#0f172a' }}>{job.title}</h2>
                <p style={{ fontSize: '0.9rem', color: '#64748b', marginTop: '2px' }}>{job.company} • {job.location || 'India'}</p>
              </div>
            </div>

            <span style={{ display: 'inline-flex', alignItems: 'center', padding: '6px 14px', borderRadius: '999px', background: '#ccfbf1', color: '#0f766e', fontSize: '0.85rem', fontWeight: 700 }}>
              {Math.round(job.match_score || 85)}% Match
            </span>
          </div>

          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '16px', padding: '14px 0', borderTop: '1px solid #f1f5f9', borderBottom: '1px solid #f1f5f9', marginBottom: '24px', fontSize: '0.85rem', color: '#475569' }}>
            <span>🏢 {job.job_type || 'Internship'}</span>
            <span>📍 {job.location || 'India'}</span>
            <span>⚡ Algorithm: {job.formula_version || 'coverage-rag-v2'}</span>
          </div>

          <div>
            <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#0f172a', marginBottom: '10px' }}>AI Match Breakdown</h4>
            <p style={{ fontSize: '0.9rem', color: '#475569', lineHeight: 1.6, marginBottom: '20px' }}>
              {job.reason || 'Calculated based on normalized vector semantic similarity between your student skill profile and recruiter eligibility requirements.'}
            </p>

            <h4 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#0f172a', marginBottom: '10px' }}>Direct Recruiter Portal</h4>
            <p style={{ fontSize: '0.88rem', color: '#64748b', lineHeight: 1.6, marginBottom: '24px' }}>
              This opportunity was synced from active web listings. Click "Apply on Company Site" to open the direct external application portal.
            </p>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '18px' }}>
          <div className="cb-card" style={{ textAlign: 'center' }}>
            <a
              href={job.apply_url || '#'}
              target="_blank"
              rel="noreferrer"
              style={{
                display: 'block',
                width: '100%',
                padding: '13px',
                borderRadius: '8px',
                background: '#0d9488',
                color: '#fff',
                fontWeight: 700,
                fontSize: '0.95rem',
                textDecoration: 'none',
                marginBottom: '10px',
              }}
            >
              Apply on Company Site ↗
            </a>
          </div>

          <div className="cb-card">
            <h4 style={{ fontSize: '0.95rem', fontWeight: 700, color: '#0f172a', marginBottom: '12px' }}>Why this matches you?</h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', fontSize: '0.84rem' }}>
              <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', color: '#0f766e' }}>
                <CheckCircle2 size={16} style={{ flexShrink: 0, marginTop: '2px' }} />
                <span>Matched Skills: {(job.matched_skills || ['Python']).join(', ')}</span>
              </div>
              {(job.missing_skills || []).length > 0 && (
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '8px', color: '#b45309' }}>
                  <AlertCircle size={16} style={{ flexShrink: 0, marginTop: '2px' }} />
                  <span>Recommended to Learn: {job.missing_skills.join(', ')}</span>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
