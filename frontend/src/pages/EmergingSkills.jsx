import { useState, useEffect } from 'react'
import Card from '../components/Card'
import SkillCard from '../components/SkillCard'
import Loading from '../components/Loading'
import Error from '../components/Error'
import { getEmergingSkills } from '../services/api'
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

  if (loading) {
    return <Loading message="Loading emerging skills..." />
  }

  if (error) {
    return <Error message={error} onRetry={loadEmergingSkills} />
  }

  return (
    <div className="emerging-page">
      <div className="page-header">
        <div>
          <h1>Emerging Skills</h1>
          <p className="page-subtitle">
            Skills with low obsolescence risk and high growth potential. These technologies show strong growth trends, increasing demand, and active community engagement. Invest in these skills for future-proof career growth.
          </p>
        </div>
      </div>

      <Card className="info-card">
        <div className="info-content">
          <span className="info-icon">✨</span>
          <div>
            <h3>What are "Emerging Skills"?</h3>
            <p>
              Emerging skills show strong growth trends, increasing demand, and active community engagement.
              These technologies are gaining traction and may be valuable additions to your skill set.
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
              <SkillCard key={skill.name} skill={skill} />
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

