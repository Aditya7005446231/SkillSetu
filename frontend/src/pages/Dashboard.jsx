import { ArrowRight, CheckCircle2, Flame, Sparkles, TrendingUp } from 'lucide-react'
import ExtractedSkills from '../components/ExtractedSkills'
import ProfileCard from '../components/ProfileCard'
import ProjectList from '../components/ProjectList'

function Dashboard({ profile, onUpload }) {
  const skillCount = profile?.skills?.length || 0
  const projectCount = profile?.projects?.length || 0
  return <div className="page-wrap dashboard-page"><section className="dashboard-hero"><div><span className="hero-chip dark"><Sparkles size={13} /> YOUR CAREER, REFRAMED</span><h2>Small steps.<br /><em>Big momentum.</em></h2><p>Your career story is more than a list of roles. Let's make it work for you.</p><button className="hero-cta" onClick={onUpload}>{profile ? 'Update your profile' : 'Build my profile'} <ArrowRight size={16} /></button></div><div className="hero-grid"><span /><span /><span /><span /></div></section><div className="metric-row"><div className="metric"><span className="metric-icon purple-metric"><TrendingUp size={17} /></span><div><small>PROFILE SIGNAL</small><strong>{profile ? 'Strong start' : 'Not started'}</strong></div></div><div className="metric"><span className="metric-icon orange-metric"><Flame size={17} /></span><div><small>SKILLS FOUND</small><strong>{skillCount || '—'} <small>{skillCount ? 'mapped' : 'upload to see'}</small></strong></div></div><div className="metric"><span className="metric-icon green-metric"><CheckCircle2 size={17} /></span><div><small>PROJECTS</small><strong>{projectCount || '—'} <small>{projectCount ? 'extracted' : 'upload to see'}</small></strong></div></div></div><div className="dashboard-grid"><div className="dashboard-main"><ProfileCard profile={profile} />{profile && <ExtractedSkills skills={profile.skills} />}</div><div className="dashboard-aside"><div className="next-card"><p className="eyebrow purple">NEXT BEST MOVE</p><h3>{profile ? 'Turn your proof into opportunity.' : 'Give your profile a signal.'}</h3><p>{profile ? 'Your projects are a great starting point. Add links and measurable outcomes to make them pop.' : 'Your resume is the fastest way to unlock a personalized career view.'}</p><button onClick={onUpload}>{profile ? 'Improve profile' : 'Upload resume'} <ArrowRight size={14} /></button></div>{profile && <ProjectList projects={profile.projects} />}</div></div></div>
}

export default Dashboard
