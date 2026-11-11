import { GraduationCap, MapPin, Target } from 'lucide-react'

function ProfileCard({ profile }) {
  if (!profile) return <section className="profile-card empty-profile"><div className="profile-orb"><Target size={23} /></div><div><p className="eyebrow purple">YOUR NORTH STAR</p><h2>Your profile is waiting</h2><p className="muted">Upload a resume and we will map your experience into a career-ready profile.</p></div></section>
  return <section className="profile-card"><div className="profile-card-top"><div className="profile-avatar">{profile.full_name?.slice(0, 2).toUpperCase() || 'SS'}</div><div><p className="eyebrow purple">PROFILE SNAPSHOT</p><h2>{profile.full_name || 'Your profile'}</h2><p className="profile-goal">{profile.career_goal || 'Career direction is taking shape.'}</p></div></div><div className="profile-meta"><span><GraduationCap size={15} /> {profile.degree || 'Degree not listed'}</span><span><MapPin size={15} /> {profile.university || 'University not listed'}</span></div></section>
}

export default ProfileCard
