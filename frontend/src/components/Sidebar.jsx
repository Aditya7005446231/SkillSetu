import { NavLink } from 'react-router-dom'
import { Bot, BriefcaseBusiness, ChartNoAxesCombined, House, Map, UserRound } from 'lucide-react'

const links = [
  { to: '/dashboard', label: 'Dashboard', icon: House },
  { to: '/profile', label: 'My profile', icon: UserRound },
  { to: '/opportunities', label: 'Opportunities', icon: BriefcaseBusiness },
  { to: '/skill-gap', label: 'Skill gap', icon: ChartNoAxesCombined },
  { to: '/roadmap', label: 'Roadmap', icon: Map },
  { to: '/assistant', label: 'AI assistant', icon: Bot },
]

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="brand"><span className="brand-mark">S</span><span>SkillSetu</span></div>
      <p className="sidebar-label">Workspace</p>
      <nav className="sidebar-nav" aria-label="Main navigation">
        {links.map(({ to, label, icon: Icon }) => (
          <NavLink key={to} to={to} className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'}>
            <Icon size={19} strokeWidth={1.8} /> {label}
          </NavLink>
        ))}
      </nav>
      <div className="sidebar-footer">
        <div className="sidebar-tip"><span>✦</span><strong>Keep growing</strong><small>Small steps make big careers.</small></div>
        <span className="sidebar-version">SkillSetu v1.0</span>
      </div>
    </aside>
  )
}

export default Sidebar
