import { ArrowRight, BookOpen, BriefcaseBusiness, CheckCircle2, Clock3, Target } from 'lucide-react'
import { Link } from 'react-router-dom'
import JobCard from '../components/JobCard'
import SkillCard from '../components/SkillCard'

const skills = [
  { name: 'React', level: 'Advanced', progress: 82, color: 'purple', icon: 'R' },
  { name: 'Product design', level: 'Intermediate', progress: 64, color: 'orange', icon: '✦' },
  { name: 'TypeScript', level: 'Intermediate', progress: 58, color: 'blue', icon: 'TS' },
]
const jobs = [
  { title: 'Frontend Engineer', company: 'Orbit Labs', location: 'Remote', type: 'Full-time', salary: '$105k – $135k' },
  { title: 'Product Designer', company: 'Northstar', location: 'New York, NY', type: 'Hybrid', salary: '$90k – $120k' },
]

function Dashboard() {
  return <div className="dashboard-page">
    <section className="welcome-banner"><div><span className="eyebrow">YOUR CAREER SNAPSHOT</span><h2>You are making great progress, Alex.</h2><p>Stay consistent and you will reach your next milestone in no time.</p><Link to="/roadmap" className="button primary">View your roadmap <ArrowRight size={16} /></Link></div><div className="banner-score"><strong>72</strong><span>Career score</span><div className="score-ring" /></div></section>
    <section className="stat-grid">
      <div className="stat-card"><span className="stat-icon purple-bg"><Target size={19} /></span><div><p>Career score</p><h3>72 <small>/ 100</small></h3></div><span className="trend">+8%</span></div>
      <div className="stat-card"><span className="stat-icon orange-bg"><BookOpen size={19} /></span><div><p>Skills mastered</p><h3>12 <small>skills</small></h3></div><span className="trend">+2</span></div>
      <div className="stat-card"><span className="stat-icon blue-bg"><BriefcaseBusiness size={19} /></span><div><p>Role matches</p><h3>24 <small>new roles</small></h3></div><span className="trend">+14%</span></div>
      <div className="stat-card"><span className="stat-icon green-bg"><Clock3 size={19} /></span><div><p>Learning streak</p><h3>7 <small>days</small></h3></div><span className="trend">Best yet</span></div>
    </section>
    <div className="content-grid"><section className="panel"><div className="section-heading"><div><h2>Skill progress</h2><p>Your strongest skills right now</p></div><Link to="/skill-gap" className="text-button">See all <ArrowRight size={15} /></Link></div>{skills.map(skill => <SkillCard key={skill.name} skill={skill} />)}</section>
      <section className="panel"><div className="section-heading"><div><h2>Next on your roadmap</h2><p>Keep your momentum going</p></div><Link to="/roadmap" className="text-button">View roadmap <ArrowRight size={15} /></Link></div><div className="timeline"><div className="timeline-item done"><span><CheckCircle2 size={17} /></span><div><strong>Complete portfolio refresh</strong><p>Completed yesterday</p></div></div><div className="timeline-item current"><span>2</span><div><strong>Build a TypeScript project</strong><p>In progress · 65% complete</p><div className="progress-track"><i style={{ width: '65%' }} /></div></div></div><div className="timeline-item"><span>3</span><div><strong>Apply to 5 frontend roles</strong><p>Up next · Due in 8 days</p></div></div></div></section></div>
    <section className="panel jobs-panel"><div className="section-heading"><div><h2>Recommended opportunities</h2><p>Based on your profile and goals</p></div><Link to="/opportunities" className="text-button">Explore all <ArrowRight size={15} /></Link></div><div className="jobs-grid">{jobs.map(job => <JobCard key={job.title} job={job} />)}</div></section>
  </div>
}
export default Dashboard
