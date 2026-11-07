import { ArrowUpRight, Bookmark, MapPin } from 'lucide-react'

function JobCard({ job }) {
  return (
    <article className="job-card">
      <div className="job-card-top"><span className="company-logo">{job.company[0]}</span><button className="bookmark" aria-label="Save job"><Bookmark size={18} /></button></div>
      <h3>{job.title}</h3><p className="company">{job.company}</p>
      <div className="job-meta"><span><MapPin size={14} /> {job.location}</span><span>{job.type}</span></div>
      <div className="job-card-bottom"><strong>{job.salary}</strong><button className="text-button">View role <ArrowUpRight size={15} /></button></div>
    </article>
  )
}

export default JobCard
