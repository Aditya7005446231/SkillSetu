import { useEffect, useState } from 'react'
import { Filter, Search } from 'lucide-react'
import JobCard from '../components/JobCard'
import { getRecommendedOpportunities } from '../services/opportunities'

function Opportunities() {
  const [jobs, setJobs] = useState([])
  const [query, setQuery] = useState('')
  const [location, setLocation] = useState('')
  const [jobType, setJobType] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    async function loadJobs() {
      setLoading(true)
      setError('')
      try {
        const filters = {}
        if (location) filters.location = location
        if (jobType) filters.job_type = jobType
        const data = await getRecommendedOpportunities(filters)
        setJobs(data.recommendations || [])
      } catch (loadError) {
        setError(loadError.response?.data?.detail || loadError.message)
      } finally {
        setLoading(false)
      }
    }
    loadJobs()
  }, [location, jobType])

  const visibleJobs = jobs.filter((job) => {
    const search = query.toLowerCase()
    return !search || `${job.title} ${job.company} ${job.location}`.toLowerCase().includes(search)
  })

  return <div>
    <div className="toolbar">
      <div className="search-field"><Search size={17} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="Search roles, companies, or skills" /></div>
      <select value={location} onChange={(event) => setLocation(event.target.value)} aria-label="Location">
        <option value="">All locations</option>
        <option value="India">India</option>
        <option value="Bengaluru">Bengaluru</option>
        <option value="Hyderabad">Hyderabad</option>
        <option value="Pune">Pune</option>
        <option value="Mumbai">Mumbai</option>
        <option value="Delhi">Delhi</option>
        <option value="Remote">Remote</option>
      </select>
      <select value={jobType} onChange={(event) => setJobType(event.target.value)} aria-label="Job type">
        <option value="">All job types</option>
        <option value="internship">Internship</option>
        <option value="full-time">Full time</option>
        <option value="part-time">Part-time</option>
        <option value="contract">Contract</option>
        <option value="freelance">Freelance</option>
        <option value="temporary">Temporary</option>
      </select>
      <button className="button outline"><Filter size={16} /> Filters</button>
    </div>
    {loading && <div className="opportunity-note">Loading personalized opportunities...</div>}
    {error && <div className="opportunity-note"><strong>Unable to load opportunities</strong><span>{error}</span></div>}
    {!loading && !error && <div className="opportunity-note"><strong>{visibleJobs.length} roles match your profile</strong><span>Sorted by relevance</span></div>}
    <div className="jobs-grid opportunities-grid">
      {visibleJobs.map(job => <JobCard key={job.job_id} job={job} />)}
    </div>
  </div>
}
export default Opportunities
