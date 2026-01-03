import { Link } from 'react-router-dom'
import './SkillCard.css'

const SkillCard = ({ skill }) => {
  const getRiskColor = (riskScore) => {
    if (riskScore >= 0.7) return 'high'
    if (riskScore >= 0.3) return 'medium'
    return 'low'
  }

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'increasing':
        return '📈'
      case 'decreasing':
        return '📉'
      default:
        return '➡️'
    }
  }

  const riskColor = getRiskColor(skill.risk_score)
  const trendIcon = getTrendIcon(skill.trend)

  return (
    <Link to={`/skills/${encodeURIComponent(skill.name)}`} className="skill-card-link">
      <div className={`skill-card risk-${riskColor}`}>
        <div className="skill-card-header">
          <h3 className="skill-name">{skill.name}</h3>
          <span className="trend-icon">{trendIcon}</span>
        </div>
        <div className="skill-card-body">
          <div className="skill-metrics">
            <div className="metric">
              <span className="metric-label">Current Demand</span>
              <span className="metric-value">{skill.current_demand.toFixed(0)}</span>
            </div>
            <div className="metric">
              <span className="metric-label">Forecast</span>
              <span className="metric-value">{skill.forecast_demand.toFixed(0)}</span>
            </div>
          </div>
          <div className="risk-indicator">
            <span className="risk-label">Risk Score</span>
            <div className="risk-bar">
              <div
                className={`risk-fill risk-${riskColor}`}
                style={{ width: `${skill.risk_score * 100}%` }}
              />
            </div>
            <span className="risk-value">{(skill.risk_score * 100).toFixed(0)}%</span>
          </div>
          <div className="skill-badge">
            <span className={`badge badge-${skill.risk_category}`}>
              {skill.risk_category.toUpperCase()}
            </span>
            <span className={`badge badge-${skill.trend}`}>
              {skill.trend}
            </span>
          </div>
        </div>
      </div>
    </Link>
  )
}

export default SkillCard



