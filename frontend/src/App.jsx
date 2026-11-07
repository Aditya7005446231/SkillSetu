import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import Navbar from './components/Navbar'
import Dashboard from './pages/Dashboard'
import Profile from './pages/Profile'
import Opportunities from './pages/Opportunities'
import SkillGap from './pages/SkillGap'
import Roadmap from './pages/Roadmap'
import Assistant from './pages/Assistant'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <div className="app-shell">
        <Sidebar />
        <div className="app-content">
          <Navbar />
          <main className="page-content">
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              <Route path="/profile" element={<Profile />} />
              <Route path="/opportunities" element={<Opportunities />} />
              <Route path="/skill-gap" element={<SkillGap />} />
              <Route path="/roadmap" element={<Roadmap />} />
              <Route path="/assistant" element={<Assistant />} />
            </Routes>
          </main>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App
