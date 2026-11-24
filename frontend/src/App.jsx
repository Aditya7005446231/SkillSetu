import { useEffect, useState } from 'react'
import { BarChart3, Bot, BriefcaseBusiness, LayoutDashboard, LogOut, Sparkles, UserRound } from 'lucide-react'
import Login from './components/Login'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import Opportunities from './pages/Opportunities'
import Assistant from './pages/Assistant'
import { signOut, supabase } from './services/supabase'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [activePage, setActivePage] = useState('dashboard')
  const [profile, setProfile] = useState(null)

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

  if (!user) return <Login />

  const displayName = user.user_metadata?.full_name || user.email?.split('@')[0] || 'there'

  return (
    <div className="app">
      <aside className="app-sidebar">
        <div className="logo"><span className="logo-mark"><Sparkles size={16} /></span> SkillSetu</div>
        <div className="sidebar-kicker">Your career space</div>
        <nav className="main-nav">
          <button className={activePage === 'dashboard' ? 'nav-item active' : 'nav-item'} onClick={() => setActivePage('dashboard')}><LayoutDashboard size={18} /> Overview</button>
          <button className={activePage === 'profile' ? 'nav-item active' : 'nav-item'} onClick={() => setActivePage('profile')}><UserRound size={18} /> My profile</button>
          <button className={activePage === 'opportunities' ? 'nav-item active' : 'nav-item'} onClick={() => setActivePage('opportunities')}><BriefcaseBusiness size={18} /> Opportunities</button>
          <button className={activePage === 'assistant' ? 'nav-item active' : 'nav-item'} onClick={() => setActivePage('assistant')}><Bot size={18} /> Career Copilot</button>
          <button className="nav-item muted-nav" disabled><BarChart3 size={18} /> Skill insights <span>Soon</span></button>
        </nav>
        <div className="sidebar-bottom">
          <div className="sidebar-prompt"><Sparkles size={16} /><strong>Build your edge</strong><p>Upload your resume to unlock personalized insights.</p></div>
          <button className="sign-out" onClick={signOut}><LogOut size={16} /> Sign out</button>
        </div>
      </aside>
      <main className="app-main">
        <header className="app-header">
          <div><p className="header-overline">SKILLSETU / {activePage === 'dashboard' ? 'OVERVIEW' : activePage === 'opportunities' ? 'OPPORTUNITIES' : activePage === 'assistant' ? 'CAREER COPILOT' : 'MY PROFILE'}</p><h1>{activePage === 'dashboard' ? `Hey ${displayName}, let's grow.` : activePage === 'opportunities' ? 'Opportunities' : activePage === 'assistant' ? 'Career Copilot' : 'Your profile'}</h1></div>
          <div className="header-user"><span className="mini-avatar">{displayName.slice(0, 2).toUpperCase()}</span><span>{displayName}</span></div>
        </header>
        {activePage === 'dashboard'
          ? <Dashboard profile={profile} onUpload={() => setActivePage('profile')} />
          : activePage === 'opportunities'
            ? <Opportunities />
            : activePage === 'assistant'
              ? <Assistant />
              : <Profile profile={profile} onProfileAnalyzed={setProfile} />}
      </main>
    </div>
  )
}

export default App
