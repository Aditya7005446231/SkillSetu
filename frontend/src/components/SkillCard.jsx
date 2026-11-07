function SkillCard({ skill }) {
  return (
    <div className="skill-card">
      <div className="skill-card-heading"><span className={`skill-icon ${skill.color}`}>{skill.icon}</span><div><h3>{skill.name}</h3><p>{skill.level}</p></div><strong>{skill.progress}%</strong></div>
      <div className="progress-track"><span style={{ width: `${skill.progress}%` }} /></div>
    </div>
  )
}

export default SkillCard
