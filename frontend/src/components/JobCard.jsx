import { ArrowUpRight, Bookmark, MapPin } from 'lucide-react'

function JobCard({ job }) {
  const companyInitial = (job.company || '?')[0].toUpperCase()
  const viewJob = () => {
    if (job.apply_url) window.open(job.apply_url, '_blank', 'noopener,noreferrer')
  }

  return (
    <article className="job-card">
      <div className="job-card-top"><span className="company-logo">{companyInitial}</span><button className="bookmark" aria-label="Save job"><Bookmark size={18} /></button></div>
      <h3>{job.title}</h3><p className="company">{job.company}</p>
      <div className="job-meta"><span><MapPin size={14} /> {job.location || 'Location not specified'}</span><span>{job.job_type || job.type || 'Other'}</span></div>
      {typeof job.match_score === 'number' && (
        <div className="job-card-bottom">
          <strong>{job.match_score}% match</strong>
          <span>{job.reason}</span>
        </div>
      )}
      <div className="job-card-bottom"><strong>{job.salary || ''}</strong><button className="text-button" onClick={viewJob}>View role <ArrowUpRight size={15} /></button></div>
    </article>
  )
}

export default JobCard
