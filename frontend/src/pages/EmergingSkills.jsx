import { useState, useEffect } from 'react'
import Card from '../components/Card'
import SkillCard from '../components/SkillCard'
import Loading from '../components/Loading'
import Error from '../components/Error'
import { getEmergingSkills } from '../services/api'
import { Sparklines, SparklinesLine } from 'react-sparklines'
import './EmergingSkills.css'

const EmergingSkills = () => {
  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadEmergingSkills()
  }, [])

  const loadEmergingSkills = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getEmergingSkills(50)
      setSkills(data)
    } catch (err) {
      console.error('Emerging skills load error:', err)
      setError(err.message || 'Failed to load emerging skills')
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <Loading message="Loading emerging skills..." />
  if (error) return <Error message={error} onRetry={loadEmergingSkills} />

  return (
    <div className="emerging-page">
      <div className="page-header">
        <div>
          <h1>Emerging Skills</h1>
          <p className="page-subtitle">
            Skills with low obsolescence risk and high growth potential.
            Focus on technologies showing increasing demand, active community engagement, and strong growth trends.
          </p>
        </div>
      </div>

      <Card className="info-card">
        <div className="info-content">
          <span className="info-icon">✨</span>
          <div>
            <h3>What are "Emerging Skills"?</h3>
            <p>
              Emerging skills are gaining traction and may be valuable additions to your skill set.
              Keep an eye on trends, demand, and community engagement.
            </p>
          </div>
        </div>
      </Card>

      <div className="skills-section">
        <div className="section-header">
          <h2>{skills.length} Emerging Skills</h2>
        </div>

        {skills.length > 0 ? (
          <div className="skills-grid">
            {skills.map((skill) => (
              <SkillCard key={skill.name} skill={skill}>
                {/* Inline mini chart for trend */}
                <div className="skill-trend-chart">
                  <Sparklines data={skill.historical_data || [skill.current_demand, skill.forecast_demand]}>
                    <SparklinesLine color="#4caf50" />
                  </Sparklines>
                  <span className="trend-label">{skill.trend}</span>
                </div>
              </SkillCard>
            ))}
          </div>
        ) : (
          <Card>
            <p className="empty-state">No emerging skills found</p>
          </Card>
        )}
      </div>
    </div>
  )
}

export default EmergingSkills
