import { useState } from 'react'
import { Briefcase, Eye, EyeOff, Lock, Mail, User, GraduationCap, Phone, CheckCircle2, ArrowRight } from 'lucide-react'
import { signIn, signUp } from '../services/supabase'

export function AuthPage({ onLoginSuccess, onStartOnboarding }) {
  const [isSignUp, setIsSignUp] = useState(false)
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [showPassword, setShowPassword] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(e) {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const action = isSignUp ? signUp : signIn
      const { data, error: authErr } = await action(email.trim().toLowerCase(), password)

      if (authErr) {
        throw authErr
      }

      // If user signed up and session is already active or user returned
      const activeUser = data?.session?.user || data?.user || { email, user_metadata: { full_name: fullName } }

      if (isSignUp) {
        // Automatically log in the user and start onboarding immediately
        if (onStartOnboarding) {
          onStartOnboarding(activeUser)
        }
      } else {
        if (onLoginSuccess && activeUser) {
          onLoginSuccess(activeUser)
        }
      }
    } catch (err) {
      setError(err.message || 'Authentication failed. Please verify your details.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh', background: '#fff' }}>
      {/* Left Hero Panel */}
      <div style={{
        flex: '1 1 45%',
        background: 'linear-gradient(135deg, #0e1e38 0%, #091325 100%)',
        color: '#fff',
        padding: '50px 60px',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        position: 'relative',
        overflow: 'hidden',
      }}>
        {/* Brand header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ width: '34px', height: '34px', background: '#0d9488', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Briefcase size={18} color="#fff" />
          </div>
          <span style={{ fontSize: '1.25rem', fontWeight: 800, letterSpacing: '-0.02em' }}>SkillSetu</span>
        </div>

        {/* Hero Content */}
        <div style={{ maxWidth: '440px', margin: '40px 0' }}>
          <h1 style={{ fontSize: '2.5rem', fontWeight: 800, lineHeight: 1.15, marginBottom: '16px' }}>
            {isSignUp ? 'Build your career journey with us.' : 'Your next opportunity starts here.'}
          </h1>
          <p style={{ color: '#94a3b8', fontSize: '1rem', lineHeight: 1.6, marginBottom: '28px' }}>
            {isSignUp
              ? 'Join thousands of students finding their dream placement and internship opportunities.'
              : 'Discover & apply for the best placement opportunities tailored for your verified skillset.'}
          </p>

          <div style={{
            background: 'rgba(255, 255, 255, 0.05)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            borderRadius: '16px',
            padding: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '16px',
          }}>
            <div style={{ width: '42px', height: '42px', borderRadius: '50%', background: '#0d9488', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
              <CheckCircle2 size={22} color="#fff" />
            </div>
            <div>
              <div style={{ fontWeight: 700, fontSize: '0.95rem' }}>AI-Powered Skill Gap Analysis</div>
              <div style={{ color: '#94a3b8', fontSize: '0.8rem', marginTop: '2px' }}>Real-time match scoring against live recruiter criteria</div>
            </div>
          </div>
        </div>

        {/* Footer Note */}
        <div style={{ color: '#64748b', fontSize: '0.82rem' }}>
          Built for students, designed for placement excellence.
        </div>
      </div>

      {/* Right Form Panel */}
      <div style={{
        flex: '1 1 55%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '50px 40px',
        background: '#f8fafc',
      }}>
        <div style={{ width: '100%', maxWidth: '420px', background: '#fff', padding: '40px', borderRadius: '16px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
          <div style={{ marginBottom: '28px' }}>
            <h2 style={{ fontSize: '1.75rem', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.02em' }}>
              {isSignUp ? 'Create Account' : 'Welcome back!'}
            </h2>
            <p style={{ color: '#64748b', fontSize: '0.88rem', marginTop: '6px' }}>
              {isSignUp ? "Let's get started with your student profile" : 'Sign in to continue to your placement dashboard'}
            </p>
          </div>

          {/* Social Auth Option */}
          <button
            type="button"
            onClick={() => {}}
            style={{
              width: '100%',
              padding: '11px',
              borderRadius: '10px',
              border: '1px solid #e2e8f0',
              background: '#fff',
              color: '#0f172a',
              fontWeight: 600,
              fontSize: '0.88rem',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '10px',
              cursor: 'pointer',
              marginBottom: '20px',
            }}
          >
            <svg width="18" height="18" viewBox="0 0 24 24"><path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/><path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/><path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/><path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/></svg>
            Continue with Google
          </button>

          <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '22px' }}>
            <div style={{ flex: 1, height: '1px', background: '#e2e8f0' }} />
            <span style={{ fontSize: '0.75rem', color: '#94a3b8', textTransform: 'uppercase', letterSpacing: '0.05em' }}>or</span>
            <div style={{ flex: 1, height: '1px', background: '#e2e8f0' }} />
          </div>

          {error && (
            <div style={{ padding: '10px 14px', borderRadius: '8px', background: '#ffe4e6', color: '#e11d48', fontSize: '0.84rem', marginBottom: '16px' }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
            {isSignUp && (
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Full Name</label>
                <div style={{ position: 'relative' }}>
                  <User size={16} color="#94a3b8" style={{ position: 'absolute', left: '12px', top: '12px' }} />
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Enter your full name"
                    style={{ width: '100%', padding: '10px 12px 10px 38px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem', outline: 'none' }}
                  />
                </div>
              </div>
            )}

            <div>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>University / Student Email</label>
              <div style={{ position: 'relative' }}>
                <Mail size={16} color="#94a3b8" style={{ position: 'absolute', left: '12px', top: '12px' }} />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@college.edu or personal email"
                  style={{ width: '100%', padding: '10px 12px 10px 38px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem', outline: 'none' }}
                />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '6px' }}>
                <label style={{ fontSize: '0.8rem', fontWeight: 600, color: '#334155' }}>Password</label>
                {!isSignUp && (
                  <a href="#forgot" style={{ fontSize: '0.78rem', color: '#0d9488', textDecoration: 'none', fontWeight: 600 }}>Forgot password?</a>
                )}
              </div>
              <div style={{ position: 'relative' }}>
                <Lock size={16} color="#94a3b8" style={{ position: 'absolute', left: '12px', top: '12px' }} />
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="At least 6 characters"
                  style={{ width: '100%', padding: '10px 38px 10px 38px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.88rem', outline: 'none' }}
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{ position: 'absolute', right: '12px', top: '11px', background: 'none', border: 'none', cursor: 'pointer', color: '#94a3b8' }}
                >
                  {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              style={{
                marginTop: '10px',
                padding: '12px',
                borderRadius: '8px',
                background: '#0d9488',
                color: '#fff',
                fontWeight: 700,
                fontSize: '0.92rem',
                border: 'none',
                cursor: loading ? 'not-allowed' : 'pointer',
                transition: 'background 0.2s',
              }}
            >
              {loading ? 'Please wait...' : isSignUp ? 'Continue to Onboarding →' : 'Sign In'}
            </button>
          </form>

          <div style={{ textAlign: 'center', marginTop: '22px', fontSize: '0.84rem', color: '#64748b' }}>
            {isSignUp ? 'Already have an account? ' : "Don't have an account? "}
            <button
              type="button"
              onClick={() => { setIsSignUp(!isSignUp); setError(''); }}
              style={{ background: 'none', border: 'none', color: '#0d9488', fontWeight: 700, cursor: 'pointer', fontSize: '0.84rem' }}
            >
              {isSignUp ? 'Sign in' : 'Create one'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export function OnboardingFlow({ user, onComplete }) {
  const [step, setStep] = useState(1)
  const [formData, setFormData] = useState({
    fullName: user?.user_metadata?.full_name || 'Aditya Raj Rai',
    phone: '+91 98765 43210',
    graduationYear: '2027',
    university: 'National Institute of Technology',
    degree: 'B.Tech Computer Science & Engineering',
    cgpa: '8.85',
    targetRole: 'Full-Stack Developer',
    selectedSkills: ['Python', 'React', 'FastAPI', 'SQL', 'Docker'],
    preferredLocation: 'Bangalore, India',
    remoteOnly: false,
  })

  const STEPS = [
    { num: 1, label: 'Personal' },
    { num: 2, label: 'Academic' },
    { num: 3, label: 'Skills' },
    { num: 4, label: 'Resume' },
    { num: 5, label: 'Preferences' },
    { num: 6, label: 'Review' },
  ]

  return (
    <div style={{ minHeight: '100vh', background: '#f8fafc', display: 'flex', flexDirection: 'column' }}>
      {/* Top Navbar */}
      <header style={{ height: '64px', background: '#fff', borderBottom: '1px solid #e2e8f0', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '0 40px' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <div style={{ width: '32px', height: '32px', background: '#0d9488', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            <Briefcase size={18} color="#fff" />
          </div>
          <span style={{ fontSize: '1.15rem', fontWeight: 800, color: '#0e1e38' }}>SkillSetu</span>
        </div>
        <button onClick={onComplete} style={{ background: 'none', border: 'none', color: '#64748b', fontSize: '0.85rem', cursor: 'pointer', fontWeight: 600 }}>
          Skip for now
        </button>
      </header>

      {/* Main Multi-Step Container */}
      <div style={{ maxWidth: '840px', width: '100%', margin: '40px auto', padding: '0 20px', flex: 1 }}>
        {/* Step Indicator */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '36px', position: 'relative' }}>
          <div style={{ position: 'absolute', top: '15px', left: '40px', right: '40px', height: '2px', background: '#e2e8f0', zIndex: 1 }} />
          {STEPS.map((s) => {
            const isCompleted = step > s.num
            const isCurrent = step === s.num
            return (
              <div key={s.num} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative', zIndex: 2 }}>
                <div style={{
                  width: '32px',
                  height: '32px',
                  borderRadius: '50%',
                  background: isCurrent ? '#0d9488' : isCompleted ? '#10b981' : '#fff',
                  border: isCurrent ? '2px solid #0d9488' : isCompleted ? '2px solid #10b981' : '2px solid #cbd5e1',
                  color: isCurrent || isCompleted ? '#fff' : '#64748b',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 700,
                  fontSize: '0.85rem',
                  boxShadow: isCurrent ? '0 0 0 4px rgba(13,148,136,0.15)' : 'none',
                }}>
                  {isCompleted ? '✓' : s.num}
                </div>
                <span style={{ fontSize: '0.75rem', fontWeight: 600, color: isCurrent ? '#0d9488' : '#64748b', marginTop: '6px' }}>
                  {s.label}
                </span>
              </div>
            )
          })}
        </div>

        {/* Step Card Content */}
        <div style={{ background: '#fff', borderRadius: '16px', border: '1px solid #e2e8f0', padding: '36px 40px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.05)' }}>
          {step === 1 && (
            <div>
              <div style={{ marginBottom: '24px' }}>
                <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#0f172a' }}>Tell us about yourself</h2>
                <p style={{ color: '#64748b', fontSize: '0.88rem', marginTop: '4px' }}>Help us personalize your placement and internship opportunities</p>
              </div>

              <div style={{ display: 'grid', gap: '16px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Full Name</label>
                  <input
                    type="text"
                    value={formData.fullName}
                    onChange={(e) => setFormData({ ...formData, fullName: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.9rem' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Phone Number</label>
                  <input
                    type="text"
                    value={formData.phone}
                    onChange={(e) => setFormData({ ...formData, phone: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.9rem' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Expected Graduation Year</label>
                  <select
                    value={formData.graduationYear}
                    onChange={(e) => setFormData({ ...formData, graduationYear: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.9rem', background: '#fff' }}
                  >
                    <option value="2025">2025</option>
                    <option value="2026">2026</option>
                    <option value="2027">2027</option>
                    <option value="2028">2028</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {step === 2 && (
            <div>
              <div style={{ marginBottom: '24px' }}>
                <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#0f172a' }}>Academic Details</h2>
                <p style={{ color: '#64748b', fontSize: '0.88rem', marginTop: '4px' }}>Recruiters use your college and branch for eligibility filtering</p>
              </div>

              <div style={{ display: 'grid', gap: '16px' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>University / College</label>
                  <input
                    type="text"
                    value={formData.university}
                    onChange={(e) => setFormData({ ...formData, university: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.9rem' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>Degree & Specialization</label>
                  <input
                    type="text"
                    value={formData.degree}
                    onChange={(e) => setFormData({ ...formData, degree: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.9rem' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#334155', marginBottom: '6px' }}>CGPA / Percentage</label>
                  <input
                    type="text"
                    value={formData.cgpa}
                    onChange={(e) => setFormData({ ...formData, cgpa: e.target.value })}
                    style={{ width: '100%', padding: '10px 14px', borderRadius: '8px', border: '1px solid #cbd5e1', fontSize: '0.9rem' }}
                  />
                </div>
              </div>
            </div>
          )}

          {step >= 3 && step <= 6 && (
            <div style={{ textAlign: 'center', padding: '20px 0' }}>
              <div style={{ width: '64px', height: '64px', borderRadius: '50%', background: '#ccfbf1', color: '#0d9488', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 16px' }}>
                <CheckCircle2 size={32} />
              </div>
              <h2 style={{ fontSize: '1.4rem', fontWeight: 800, color: '#0f172a' }}>You are all set!</h2>
              <p style={{ color: '#64748b', fontSize: '0.9rem', maxWidth: '440px', margin: '8px auto 24px' }}>
                Your initial profile details have been configured. You can now explore AI job matches, track applications, and build your learning roadmap.
              </p>
            </div>
          )}

          {/* Action buttons */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '32px', paddingTop: '20px', borderTop: '1px solid #f1f5f9' }}>
            {step > 1 ? (
              <button
                type="button"
                onClick={() => setStep(step - 1)}
                style={{ padding: '9px 18px', borderRadius: '8px', border: '1px solid #cbd5e1', background: '#fff', color: '#334155', fontWeight: 600, fontSize: '0.88rem', cursor: 'pointer' }}
              >
                Back
              </button>
            ) : <div />}

            <div style={{ display: 'flex', gap: '12px' }}>
              <button
                type="button"
                onClick={onComplete}
                style={{ padding: '9px 18px', borderRadius: '8px', border: 'none', background: 'transparent', color: '#64748b', fontWeight: 600, fontSize: '0.88rem', cursor: 'pointer' }}
              >
                Skip for now
              </button>
              <button
                type="button"
                onClick={() => {
                  if (step < 3) {
                    setStep(step + 1)
                  } else {
                    onComplete()
                  }
                }}
                style={{
                  padding: '9px 24px',
                  borderRadius: '8px',
                  border: 'none',
                  background: '#0d9488',
                  color: '#fff',
                  fontWeight: 700,
                  fontSize: '0.88rem',
                  cursor: 'pointer',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                }}
              >
                {step >= 3 ? 'Go to Dashboard →' : 'Next →'}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
