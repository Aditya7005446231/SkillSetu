import { ArrowUpRight, FolderKanban } from 'lucide-react'

function ProjectList({ projects = [] }) {
  return <section className="data-card projects-card"><div className="card-title-row"><div><p className="eyebrow orange">YOUR WORK</p><h2>Projects that stand out</h2></div><FolderKanban className="section-icon orange-text" size={20} /></div>{projects.length === 0 ? <div className="empty-state">Your extracted projects will appear here.</div> : <div className="project-list">{projects.map((project, index) => <article className="project-item" key={`${project.title}-${index}`}><span className="project-number">0{index + 1}</span><div><h3>{project.title}</h3><p>{project.description}</p>{project.github_url && <a href={project.github_url} target="_blank" rel="noreferrer">View repository <ArrowUpRight size={13} /></a>}</div></article>)}</div>}</section>
}

export default ProjectList
