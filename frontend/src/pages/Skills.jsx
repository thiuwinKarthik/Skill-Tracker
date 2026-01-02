import { useState, useEffect } from 'react'
import { useSearchParams } from 'react-router-dom'
import Card from '../components/Card'
import SkillCard from '../components/SkillCard'
import Loading from '../components/Loading'
import Error from '../components/Error'
import { getSkills } from '../services/api'
import './Skills.css'

const Skills = () => {
  const [skills, setSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchParams, setSearchParams] = useSearchParams()
  const [filter, setFilter] = useState(searchParams.get('filter') || 'all')
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    loadSkills()
  }, [filter])

  const loadSkills = async () => {
    try {
      setLoading(true)
      setError(null)

      const params = {}
      if (filter === 'high-risk') {
        params.min_risk = 0.7
      } else if (filter === 'low-risk') {
        params.max_risk = 0.3
      }

      const data = await getSkills(params)
      setSkills(data)
    } catch (err) {
      console.error('Skills load error:', err)
      setError(err.message || 'Failed to load skills')
    } finally {
      setLoading(false)
    }
  }

  const handleFilterChange = (newFilter) => {
    setFilter(newFilter)
    setSearchParams({ filter: newFilter })
  }

  const filteredSkills = skills.filter(skill =>
    skill.name.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return <Loading message="Loading skills..." />
  }

  if (error) {
    return <Error message={error} onRetry={loadSkills} />
  }

  return (
    <div className="skills-page">
      <div className="skills-header">
        <div>
          <h1>All Skills</h1>
          <p className="skills-subtitle">
            Browse all tracked skills and their obsolescence risk scores. Filter and search to find the skills you're interested in.
          </p>
        </div>
      </div>

      <Card className="filters-card">
        <div className="filters">
          <div className="search-box">
            <input
              type="text"
              placeholder="Search skills..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="search-input"
            />
          </div>
          <div className="filter-buttons">
            <button
              className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
              onClick={() => handleFilterChange('all')}
            >
              All
            </button>
            
          </div>
        </div>
      </Card>

      <div className="skills-results">
        <div className="results-header">
          <p className="results-count">
            {filteredSkills.length} skill{filteredSkills.length !== 1 ? 's' : ''} found
          </p>
        </div>
        {filteredSkills.length > 0 ? (
          <div className="skills-grid">
            {filteredSkills.map((skill) => (
              <SkillCard key={skill.name} skill={skill} />
            ))}
          </div>
        ) : (
          <Card>
            <p className="empty-state">No skills found matching your criteria</p>
          </Card>
        )}
      </div>
    </div>
  )
}

export default Skills

