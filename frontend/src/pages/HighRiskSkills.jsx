import { useState, useEffect } from 'react'
import Card from '../components/Card'
import SkillCard from '../components/SkillCard'
import Loading from '../components/Loading'
import Error from '../components/Error'
import { getHighRiskSkills } from '../services/api'
import './HighRiskSkills.css'

const HighRiskSkills = () => {
  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadHighRiskSkills()
  }, [])

  const loadHighRiskSkills = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getHighRiskSkills(50)
      setSkills(data)
    } catch (err) {
      console.error('High risk skills load error:', err)
      setError(err.message || 'Failed to load high-risk skills')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <Loading message="Loading high-risk skills..." />
  }

  if (error) {
    return <Error message={error} onRetry={loadHighRiskSkills} />
  }

  return (
    <div className="high-risk-page">
      <div className="page-header">
        <div>
          <h1>High Risk Skills</h1>
          <p className="page-subtitle">
            Skills with high obsolescence risk (≥70%). These technologies show declining demand, reduced community activity, or negative growth trends. Consider upskilling or transitioning to emerging alternatives.
          </p>
        </div>
      </div>

      <Card className="info-card">
        <div className="info-content">
          <span className="info-icon">⚠️</span>
          <div>
            <h3>What does "High Risk" mean?</h3>
            <p>
              High-risk skills show declining demand, reduced community activity, or negative growth trends.
              This doesn't mean the skill is obsolete, but it may be worth considering alternatives or
              complementary technologies.
            </p>
          </div>
        </div>
      </Card>

      <div className="skills-section">
        <div className="section-header">
          <h2>{skills.length} High Risk Skills</h2>
        </div>
        {skills.length > 0 ? (
          <div className="skills-grid">
            {skills.map((skill) => (
              <SkillCard key={skill.name} skill={skill} />
            ))}
          </div>
        ) : (
          <Card>
            <p className="empty-state">No high-risk skills found</p>
          </Card>
        )}
      </div>
    </div>
  )
}

export default HighRiskSkills

