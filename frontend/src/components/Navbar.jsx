import { Bell, Search } from 'lucide-react'
import { useLocation } from 'react-router-dom'

const titles = {
  '/dashboard': ['Good morning, Alex', 'Here is your career progress today.'],
  '/profile': ['Your profile', 'Keep your profile up to date to get better matches.'],
  '/opportunities': ['Opportunities for you', 'Roles that match your skills and ambitions.'],
  '/skill-gap': ['Your skill gap', 'Turn your gaps into a focused learning plan.'],
  '/roadmap': ['Your roadmap', 'A practical path towards your next career milestone.'],
  '/assistant': ['AI career assistant', 'Ask anything about your career journey.'],
}

function Navbar() {
  const { pathname } = useLocation()
  const [title, subtitle] = titles[pathname] || titles['/dashboard']
  return (
    <header className="topbar">
      <div><h1>{title}</h1><p>{subtitle}</p></div>
      <div className="topbar-actions">
        <button className="icon-button" aria-label="Search"><Search size={19} /></button>
        <button className="icon-button notification" aria-label="Notifications"><Bell size={19} /><i /></button>
        <div className="user-chip"><span className="avatar">AS</span><span className="user-name">Alex Smith</span></div>
      </div>
    </header>
  )
}

export default Navbar
