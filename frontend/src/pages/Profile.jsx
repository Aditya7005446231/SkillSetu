import { useState } from 'react'
import { ArrowLeft, Sparkles, Plus, Edit3 } from 'lucide-react'
import ResumeUpload from '../components/ResumeUpload'
import ExtractedSkills from '../components/ExtractedSkills'
import ProjectList from '../components/ProjectList'
import ResumeHub from '../components/ResumeHub'
import ManualProfileModal from '../components/ManualProfileModal'

function Profile({ profile, onProfileAnalyzed }) {
  const [showManualModal, setShowManualModal] = useState(false)
  const [hubKey, setHubKey] = useState(0)

  function handleProfileUpdated(newProfile) {
    if (onProfileAnalyzed) {
      onProfileAnalyzed(newProfile)
    }
    setHubKey((prev) => prev + 1)
  }

  return (
    <div className="page-wrap profile-page">
      <button className="back-link" type="button" onClick={() => window.history.back()}>
        <ArrowLeft size={15} /> Back to overview
      </button>

      <section className="profile-hero">
        <div>
          <span className="hero-chip"><Sparkles size={13} /> AI & Multi-Track Profile Builder</span>
          <h2>Make your experience<br /><em>impossible to miss.</em></h2>
          <p>Target multiple roles with dedicated resumes or customize your profile manually.</p>
        </div>
        <div className="hero-shape"><i /><i /><i /></div>
      </section>

      {/* Multi-Resume Management Hub */}
      <ResumeHub
        key={hubKey}
        onResumeSwitched={(activeRes) => handleProfileUpdated(activeRes.parsed_profile)}
        onOpenManualModal={() => setShowManualModal(true)}
      />

      <div className="profile-layout">
        <ResumeUpload
          onAnalyzed={(resProfile) => handleProfileUpdated(resProfile)}
        />
        <div className="profile-side-note">
          <span>✦</span>
          <strong>Multi-Resume Intelligence</strong>
          <p>
            Upload different resumes for different job searches (e.g. Frontend vs AI/ML).
            Or click <strong>"Add Profile Manually"</strong> to test without uploading a document.
          </p>
          <button
            type="button"
            onClick={() => setShowManualModal(true)}
            style={{
              marginTop: '0.75rem',
              width: '100%',
              padding: '0.5rem',
              background: '#263554',
              color: '#a5b4fc',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '0.8rem',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              gap: '6px',
            }}
          >
            <Edit3 size={13} /> Enter Details Manually
          </button>
        </div>
      </div>

      {profile && (
        <div className="results-grid">
          <ExtractedSkills skills={profile.skills} />
          <ProjectList projects={profile.projects} />
        </div>
      )}

      {showManualModal && (
        <ManualProfileModal
          onClose={() => setShowManualModal(false)}
          onProfileSaved={(savedProfile) => handleProfileUpdated(savedProfile)}
        />
      )}
    </div>
  )
}

export default Profile
