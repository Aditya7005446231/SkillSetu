import { Filter, Search } from 'lucide-react'
import JobCard from '../components/JobCard'
const jobs = [
  { title: 'Frontend Engineer', company: 'Orbit Labs', location: 'Remote', type: 'Full-time', salary: '$105k – $135k' },
  { title: 'Product Designer', company: 'Northstar', location: 'New York, NY', type: 'Hybrid', salary: '$90k – $120k' },
  { title: 'React Developer', company: 'Brightside', location: 'Austin, TX', type: 'Full-time', salary: '$100k – $130k' },
  { title: 'UI Engineer', company: 'Vercel', location: 'Remote', type: 'Full-time', salary: '$115k – $150k' },
]
function Opportunities() {
  return <div><div className="toolbar"><div className="search-field"><Search size={17} /><input placeholder="Search roles, companies, or skills" /></div><button className="button outline"><Filter size={16} /> Filters</button></div><div className="opportunity-note"><strong>24 roles match your profile</strong><span>Updated just now · Sorted by relevance</span></div><div className="jobs-grid opportunities-grid">{jobs.map(job => <JobCard key={job.title} job={job} />)}</div></div>
}
export default Opportunities
