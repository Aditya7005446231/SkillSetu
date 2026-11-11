import { ArrowLeft, Sparkles } from 'lucide-react'
import ResumeUpload from '../components/ResumeUpload'
import ExtractedSkills from '../components/ExtractedSkills'
import ProjectList from '../components/ProjectList'

function Profile({ profile, onProfileAnalyzed }) {
  return <div className="page-wrap profile-page"><button className="back-link" type="button" onClick={() => window.history.back()}><ArrowLeft size={15} /> Back to overview</button><section className="profile-hero"><div><span className="hero-chip"><Sparkles size={13} /> AI-powered profile builder</span><h2>Make your experience<br /><em>impossible to miss.</em></h2><p>Upload once. Get a sharper view of your strengths, projects, and next move.</p></div><div className="hero-shape"><i /><i /><i /></div></section><div className="profile-layout"><ResumeUpload onAnalyzed={onProfileAnalyzed} /><div className="profile-side-note"><span>✦</span><strong>Private by design</strong><p>Your resume is only used to personalize your experience. You control what comes next.</p></div></div>{profile && <div className="results-grid"><ExtractedSkills skills={profile.skills} /><ProjectList projects={profile.projects} /></div>}</div>
}

export default Profile
