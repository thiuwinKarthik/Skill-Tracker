import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import Card from '../components/Card'
import Loading from '../components/Loading'
import Error from '../components/Error'
import { getSkillDetail } from '../services/api'
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import './SkillDetail.css'

const SkillDetail = () => {
  const { skillName } = useParams()
  const [skill, setSkill] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadSkillDetail()
  }, [skillName])

  const loadSkillDetail = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getSkillDetail(skillName)
      setSkill(data)
    } catch (err) {
      console.error('Skill detail load error:', err)
      setError(err.message || 'Failed to load skill details')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <Loading message="Loading skill details..." />
  }

  if (error) {
    return <Error message={error} onRetry={loadSkillDetail} />
  }

  if (!skill) {
    return <Error message="Skill not found" />
  }

  const getRiskColor = (riskScore) => {
    if (riskScore >= 0.7) return 'high'
    if (riskScore >= 0.3) return 'medium'
    return 'low'
  }

  const riskColor = getRiskColor(skill.risk_score)

  // Mock historical data for visualization
  const historicalData = [
    { date: '2024-01', demand: skill.current_demand * 0.8, risk: skill.risk_score * 0.9 },
    { date: '2024-02', demand: skill.current_demand * 0.85, risk: skill.risk_score * 0.95 },
    { date: '2024-03', demand: skill.current_demand * 0.9, risk: skill.risk_score },
    { date: '2024-04', demand: skill.current_demand, risk: skill.risk_score },
    { date: '2024-05', demand: skill.forecast_demand, risk: skill.risk_score * 1.05 },
  ]

  return (
    <div className="skill-detail">
      <Link to="/skills" className="back-link">← Back to Skills</Link>

      <div className="skill-detail-header">
        <div className="skill-header-info">
          <h1>{skill.name}</h1>
          {/* {skill.category && (
            <div className="skill-category-tag">{skill.category}</div>
          )} */}
        </div>
        <div className={`risk-badge-large risk-${riskColor}`}>
          <span className="risk-label-large">Risk Score</span>
          <span className="risk-value-large">{(skill.risk_score * 100).toFixed(0)}%</span>
        </div>
      </div>

      {/* Skill Description Section */}
      {skill.description && (
        <Card className="description-card">
          <div className="description-header">
            <h2>About {skill.name}</h2>
            <div className="skill-meta">
              {skill.category && (
                <span className="meta-badge category">{skill.category}</span>
              )}
              {skill.popularity && (
                <span className={`meta-badge popularity popularity-${skill.popularity.toLowerCase().replace(' ', '-')}`}>
                  {skill.popularity} Popularity
                </span>
              )}
              {skill.trend_info && (
                <span className={`meta-badge trend-info trend-${skill.trend_info.toLowerCase()}`}>
                  {skill.trend_info} Trend
                </span>
              )}
            </div>
          </div>
          <p className="skill-description">{skill.description}</p>
        </Card>
      )}

      <div className="skill-detail-grid">
        <Card title="Overview" className="overview-card">
          <div className="overview-metrics">
            <div className="overview-metric">
              <span className="metric-label">Current Demand</span>
              <span className="metric-value-large">{skill.current_demand.toFixed(0)}</span>
            </div>
            <div className="overview-metric">
              <span className="metric-label">Forecasted Demand</span>
              <span className="metric-value-large">{skill.forecast_demand.toFixed(0)}</span>
            </div>
            <div className="overview-metric">
              <span className="metric-label">Trend</span>
              <span className={`trend-badge trend-${skill.trend}`}>
                {skill.trend}
              </span>
            </div>
            <div className="overview-metric">
              <span className="metric-label">Risk Category</span>
              <span className={`risk-category-badge risk-${skill.risk_category}`}>
                {skill.risk_category.toUpperCase()}
              </span>
            </div>
          </div>
        </Card>
        <Card title="Demand Trend" className="chart-card">
          <ResponsiveContainer width="100%" height={250}>
            <AreaChart data={historicalData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Area type="monotone" dataKey="demand" stroke="#6366f1" fill="#6366f1" fillOpacity={0.3} name="Demand" />
            </AreaChart>
          </ResponsiveContainer>
        </Card>

        <Card title="Risk Trend" className="chart-card">
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={historicalData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="risk" stroke="#ef4444" strokeWidth={2} name="Risk Score" />
            </LineChart>
          </ResponsiveContainer>
        </Card>

        {skill.related_skills && skill.related_skills.length > 0 && (
          <Card title="Related Skills" className="related-skills-card">
            <div className="related-skills-list">
              {skill.related_skills.map((relatedSkill, index) => (
                <Link
                  key={index}
                  to={`/skills/${encodeURIComponent(relatedSkill)}`}
                  className="related-skill-link"
                >
                  {relatedSkill}
                </Link>
              ))}
            </div>
          </Card>
        )}
      </div>
    </div>
  )
}

export default SkillDetail

