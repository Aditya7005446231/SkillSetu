import { Code2, Layers3, UsersRound } from 'lucide-react'

const icons = { technical: Code2, soft: UsersRound, default: Layers3 }

function ExtractedSkills({ skills = [] }) {
  const groups = skills.reduce((result, skill) => {
    const category = skill.category || 'Other'
    const key = category.toLowerCase().includes('soft') ? 'soft' : category.toLowerCase().includes('technical') ? 'technical' : 'default'
    result[key] ||= { label: category, skills: [] }
    result[key].skills.push(skill)
    return result
  }, {})

  return <section className="data-card skills-card"><div className="card-title-row"><div><p className="eyebrow purple">SIGNAL FOUND</p><h2>Your skill stack</h2></div><span className="count-badge">{skills.length} skills</span></div>{skills.length === 0 ? <div className="empty-state">Upload your resume to reveal your strongest skills.</div> : <div className="skill-groups">{Object.values(groups).map((group) => { const Icon = icons[group.skills[0].category?.toLowerCase().includes('soft') ? 'soft' : group.skills[0].category?.toLowerCase().includes('technical') ? 'technical' : 'default']; return <div className="skill-group" key={group.label}><div className="group-label"><Icon size={15} /> {group.label}</div><div className="skill-pills">{group.skills.map((skill) => <span className="skill-pill" key={`${skill.name}-${skill.category}`}><b>{skill.name}</b><small>{skill.proficiency}</small></span>)}</div></div> })}</div>}</section>
}

export default ExtractedSkills
