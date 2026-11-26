import { useEffect, useState } from 'react'
import { ArrowUpRight, BarChart3, Building2, CheckCircle2, Info, Lightbulb, TrendingUp } from 'lucide-react'
import { getInstitutionalSkills } from '../services/opportunities'

function SkillGap() {
  const [instData, setInstData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getInstitutionalSkills()
        setInstData(data)
      } catch (err) {
        console.error('Failed loading institutional data:', err)
      } finally {
        setLoading(false)
      }
    }
    loadData()
  }, [])

  return (
    <div className="skill-gap-page">
      {/* Institutional Placement Demand Banner */}
      <section className="gap-summary panel" style={{ background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)', color: '#fff' }}>
        <div>
          <span className="eyebrow" style={{ color: '#38bdf8' }}>
            <Building2 size={13} style={{ display: 'inline', marginRight: '4px' }} />
            [Simulated Demo] {instData?.institution_name || 'Campus Training & Placement Cell'}
          </span>
          <h2 style={{ color: '#fff', marginTop: '0.4rem' }}>Campus Placement Demand Analytics (2026-27)</h2>
          <p style={{ color: '#94a3b8' }}>
            Real-time hiring demand compiled from {instData?.active_recruiting_partners || 48} active partner recruiters across {instData?.total_active_openings || 320} current openings.
          </p>
        </div>
        <div className="gap-score" style={{ borderLeft: '1px solid rgba(255,255,255,0.1)' }}>
          <strong style={{ color: '#38bdf8' }}>{instData?.total_active_openings || 320}</strong>
          <span style={{ color: '#94a3b8' }}>Active Openings</span>
        </div>
      </section>

      {/* Role Demand Breakdown */}
      {instData?.role_demand_breakdown && (
        <section className="panel" style={{ marginTop: '1.25rem' }}>
          <div className="section-heading">
            <div>
              <h2>Recruiting Roles Distribution</h2>
              <p>Breakdown of active hiring demand by technology role across visiting campus companies.</p>
            </div>
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '1rem', marginTop: '0.75rem' }}>
            {Object.entries(instData.role_demand_breakdown).map(([role, pct]) => (
              <div key={role} style={{ padding: '0.85rem', background: '#f8fafc', borderRadius: '8px', border: '1px solid #e2e8f0' }}>
                <span style={{ fontSize: '0.78rem', color: '#64748b', fontWeight: 500 }}>{role}</span>
                <div style={{ display: 'flex', alignItems: 'baseline', justifyContent: 'space-between', marginTop: '0.25rem' }}>
                  <strong style={{ fontSize: '1.25rem', color: '#0f172a' }}>{pct}%</strong>
                  <span style={{ fontSize: '0.72rem', color: '#0284c7', background: '#e0f2fe', padding: '0.1rem 0.4rem', borderRadius: '4px' }}>In demand</span>
                </div>
                <div className="progress-track" style={{ marginTop: '0.5rem', height: '6px' }}>
                  <span style={{ width: `${pct}%`, background: '#0284c7' }} />
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Top Skills Demand Grid */}
      <div className="content-grid" style={{ marginTop: '1.25rem' }}>
        <section className="panel">
          <div className="section-heading">
            <div>
              <h2>Top Employer Demanded Skills</h2>
              <p>Percentage of campus recruiters screening candidates for these skills.</p>
            </div>
          </div>

          {instData?.top_demanded_skills?.map((item) => (
            <div className="gap-item" key={item.skill} style={{ marginBottom: '1rem' }}>
              <div className="gap-item-heading" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <h3 style={{ fontSize: '0.95rem', fontWeight: 600 }}>{item.skill}</h3>
                  <p style={{ fontSize: '0.78rem', color: '#64748b' }}>
                    {item.category} · {item.openings_count} openings
                  </p>
                </div>
                <div style={{ textAlign: 'right' }}>
                  <span style={{ fontWeight: 700, fontSize: '0.95rem', color: '#0f172a' }}>{item.demand_percentage}%</span>
                  <span style={{ display: 'block', fontSize: '0.72rem', color: '#16a34a', fontWeight: 500 }}>
                    <TrendingUp size={11} style={{ display: 'inline', marginRight: '2px' }} />
                    {item.yoy_growth} YoY
                  </span>
                </div>
              </div>
              <div className="progress-track" style={{ height: '7px', marginTop: '0.35rem' }}>
                <span
                  style={{
                    width: `${item.demand_percentage}%`,
                    background: item.demand_percentage > 80 ? '#0284c7' : item.demand_percentage > 60 ? '#38bdf8' : '#94a3b8'
                  }}
                />
              </div>
            </div>
          ))}
        </section>

        {/* Advisory and Curriculum Gap Recommendations */}
        <section className="panel learning-panel">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
            <Lightbulb size={22} style={{ color: '#f59e0b' }} />
            <h2 style={{ fontSize: '1.1rem', margin: 0 }}>Placement Cell Advisory</h2>
          </div>
          <p style={{ fontSize: '0.85rem', color: '#475569', marginBottom: '1rem' }}>
            Strategic recommendations from placement coordinators based on employer hiring patterns:
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {instData?.curriculum_gap_recommendations?.map((rec, i) => (
              <div
                key={i}
                style={{
                  padding: '0.75rem',
                  background: '#fff',
                  borderRadius: '6px',
                  border: '1px solid #e2e8f0',
                  fontSize: '0.825rem',
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.5rem',
                  lineHeight: '1.4'
                }}
              >
                <CheckCircle2 size={16} style={{ color: '#0284c7', flexShrink: 0, marginTop: '2px' }} />
                <span>{rec}</span>
              </div>
            ))}
          </div>

          <div style={{ marginTop: '1.25rem', padding: '0.75rem', background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: '6px' }}>
            <span style={{ fontSize: '0.78rem', color: '#166534', fontWeight: 600 }}>Mock Label Notice:</span>
            <p style={{ fontSize: '0.75rem', color: '#15803d', margin: '0.2rem 0 0 0' }}>
              {instData?.notice || 'Simulated university training & placement cell analytics.'}
            </p>
          </div>
        </section>
      </div>
    </div>
  )
}

export default SkillGap
