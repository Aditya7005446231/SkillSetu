import { useEffect, useState } from 'react'
import {
  BarChart2,
  BookOpen,
  Bot,
  Briefcase,
  CheckCircle,
  ChevronRight,
  FileText,
  Layers,
  LayoutDashboard,
  LogOut,
  MapPin,
  Search,
  Send,
  Sparkles,
  TrendingUp,
  User,
} from 'lucide-react'

import { signOut, supabase } from './services/supabase'
import './styles/careerbridge.css'

// Modular CareerBridge Screens
import { AuthPage, OnboardingFlow } from './components/AuthAndOnboarding'
import { MainDashboard, JobOpportunitiesPage, JobDetailsView } from './components/MainAndOpportunities'
import { MyApplicationsPage, SkillAnalysisPage, LearningRoadmapPage } from './components/ApplicationsAndAnalysis'
import { ProfileSettingsPage, CareerAssistantChatPage, EmptyAndSuccessStates } from './components/ProfileAssistantAndStates'
import { ThemeSwitcher } from './components/ThemeSwitcher'
import SkillGap from './pages/SkillGap'

function App() {
  const [user, setUser] = useState(null)
  const [isOnboarding, setIsOnboarding] = useState(false)
  const [activePage, setActivePage] = useState('dashboard')
  const [selectedJob, setSelectedJob] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')

  useEffect(() => {
    supabase.auth.getSession().then(({ data, error }) => {
      if (error) console.error('Unable to read Supabase session:', error)
      setUser(data?.session?.user ?? null)
    })

    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null)
    })

    return () => subscription.unsubscribe()
  }, [])

  // If user is not authenticated and not in onboarding, show modern Login / Registration screen
  if (!user && !isOnboarding) {
    return (
      <AuthPage
        onLoginSuccess={(u) => setUser(u)}
        onStartOnboarding={(newUser) => {
          setUser(newUser)
          setIsOnboarding(true)
        }}
      />
    )
  }

  // If user triggered onboarding flow
  if (isOnboarding) {
    return (
      <OnboardingFlow
        user={user}
        onComplete={() => {
          setIsOnboarding(false)
          setActivePage('dashboard')
        }}
      />
    )
  }

  const studentName = user?.user_metadata?.full_name || user?.email?.split('@')[0] || 'Aditya Raj Rai'

  return (
    <div className="cb-app-shell">
      {/* Deep Navy Left Sidebar */}
      <aside className="cb-sidebar">
        <div className="cb-sidebar-brand">
          <div className="cb-brand-icon">
            <Briefcase size={18} />
          </div>
          <span className="cb-brand-title">SkillSetu</span>
        </div>

        {/* Navigation Group 1: General */}
        <div className="cb-nav-group">
          <button
            className={`cb-nav-link ${activePage === 'dashboard' ? 'active' : ''}`}
            onClick={() => { setActivePage('dashboard'); setSelectedJob(null); }}
          >
            <LayoutDashboard size={17} />
            <span>Overview</span>
          </button>

          <button
            className={`cb-nav-link ${activePage === 'opportunities' || activePage === 'job-details' ? 'active' : ''}`}
            onClick={() => { setActivePage('opportunities'); setSelectedJob(null); }}
          >
            <Search size={17} />
            <span>Explore Opportunities</span>
          </button>

          <button
            className={`cb-nav-link ${activePage === 'applications' ? 'active' : ''}`}
            onClick={() => { setActivePage('applications'); setSelectedJob(null); }}
          >
            <Send size={17} />
            <span>My Applications</span>
            <span className="cb-nav-badge">Demo</span>
          </button>
        </div>

        {/* Navigation Group 2: Career Development */}
        <div className="cb-nav-group">
          <div className="cb-nav-label">Career Development</div>

          <button
            className={`cb-nav-link ${activePage === 'profile' ? 'active' : ''}`}
            onClick={() => { setActivePage('profile'); setSelectedJob(null); }}
          >
            <User size={17} />
            <span>My Profile</span>
          </button>

          <button
            className={`cb-nav-link ${activePage === 'skill-analysis' ? 'active' : ''}`}
            onClick={() => { setActivePage('skill-analysis'); setSelectedJob(null); }}
          >
            <BarChart2 size={17} />
            <span>Skill Analysis</span>
          </button>

          <button
            className={`cb-nav-link ${activePage === 'learning-roadmap' ? 'active' : ''}`}
            onClick={() => { setActivePage('learning-roadmap'); setSelectedJob(null); }}
          >
            <BookOpen size={17} />
            <span>Learning Roadmap</span>
          </button>

          <button
            className={`cb-nav-link ${activePage === 'assistant' ? 'active' : ''}`}
            onClick={() => { setActivePage('assistant'); setSelectedJob(null); }}
          >
            <Bot size={17} />
            <span>Career Assistant</span>
          </button>

          <button
            className={`cb-nav-link ${activePage === 'insights' ? 'active' : ''}`}
            onClick={() => { setActivePage('insights'); setSelectedJob(null); }}
          >
            <Sparkles size={17} />
            <span>Campus T&P Demand</span>
          </button>

          <button
            className={`cb-nav-link ${activePage === 'states-preview' ? 'active' : ''}`}
            onClick={() => { setActivePage('states-preview'); setSelectedJob(null); }}
          >
            <Layers size={17} />
            <span>States Preview</span>
          </button>
        </div>

        {/* Bottom User Card */}
        <div className="cb-sidebar-footer">
          <div className="cb-user-chip">
            <div className="cb-user-avatar">
              {studentName.slice(0, 2).toUpperCase()}
            </div>
            <div className="cb-user-info">
              <div className="cb-user-name">{studentName}</div>
              <div className="cb-user-role">Student</div>
            </div>
            <button className="cb-signout-btn" onClick={signOut} title="Sign Out">
              <LogOut size={16} />
            </button>
          </div>
        </div>
      </aside>

      {/* Main Workspace Area */}
      <div className="cb-main-area">
        {/* Top Header Bar */}
        <header className="cb-topbar">
          <div className="cb-search-bar">
            <Search size={16} />
            <input
              type="text"
              placeholder="Search jobs, skills, roles..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div className="cb-topbar-actions">
            <ThemeSwitcher />
            <span className="cb-badge-pill cb-badge-teal">
              <Sparkles size={13} /> AI Placement Ready
            </span>
          </div>
        </header>

        {/* Routed Screen Content */}
        {activePage === 'dashboard' && (
          <MainDashboard
            studentName={studentName}
            onNavigate={(page, job) => {
              if (job) setSelectedJob(job)
              setActivePage(page)
            }}
          />
        )}

        {activePage === 'opportunities' && (
          <JobOpportunitiesPage
            onSelectJob={(job) => {
              setSelectedJob(job)
              setActivePage('job-details')
            }}
          />
        )}

        {activePage === 'job-details' && (
          <JobDetailsView
            job={selectedJob || {
              title: 'Software Engineer Intern',
              company: 'Microsoft',
              location: 'Bengaluru',
              matchScore: 92,
            }}
            onBack={() => setActivePage('opportunities')}
            onApply={() => setActivePage('states-preview')}
          />
        )}

        {activePage === 'applications' && (
          <MyApplicationsPage
            onExploreMore={() => setActivePage('opportunities')}
          />
        )}

        {activePage === 'skill-analysis' && <SkillAnalysisPage />}

        {activePage === 'learning-roadmap' && <LearningRoadmapPage />}

        {activePage === 'profile' && (
          <ProfileSettingsPage studentName={studentName} />
        )}

        {activePage === 'assistant' && <CareerAssistantChatPage />}

        {activePage === 'insights' && <SkillGap />}

        {activePage === 'states-preview' && (
          <EmptyAndSuccessStates
            onExplore={() => setActivePage('opportunities')}
          />
        )}
      </div>
    </div>
  )
}

export default App
