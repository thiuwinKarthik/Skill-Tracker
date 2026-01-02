import { useState, useEffect } from 'react'
import Card from '../components/Card'
import Loading from '../components/Loading'
import Error from '../components/Error'
import { getRoleTrends } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts'
import './RoleTrends.css'

const RoleTrends = () => {
  const [roles, setRoles] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    loadRoleTrends()
  }, [])

  const loadRoleTrends = async () => {
    try {
      setLoading(true)
      setError(null)
      const data = await getRoleTrends()
      setRoles(data)
    } catch (err) {
      console.error('Role trends load error:', err)
      setError(err.message || 'Failed to load role trends')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <Loading message="Loading role trends..." />
  }

  if (error) {
    return <Error message={error} onRetry={loadRoleTrends} />
  }

  const chartData = roles.map(role => ({
    name: role.name,
    skills: role.required_skills.length,
    trend: role.demand_trend === 'increasing' ? 1 : role.demand_trend === 'decreasing' ? -1 : 0
  }))

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'increasing':
        return '#10b981'
      case 'decreasing':
        return '#ef4444'
      default:
        return '#6b7280'
    }
  }

  return (
    <div className="role-trends-page">
      <div className="page-header">
        <div>
          <h1>Role Trends</h1>
          <p className="page-subtitle">
            Explore technology roles and their required skill sets. Understand which skills are in demand for different career paths and how role requirements are evolving.
          </p>
        </div>
      </div>

      <Card title="Role Demand Overview" className="chart-card">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="skills" fill="#6366f1" name="Required Skills Count" />
          </BarChart>
        </ResponsiveContainer>
      </Card>

      <div className="roles-grid">
        {roles.map((role) => (
          <Card key={role.name} className="role-card">
            <div className="role-header">
              <h3 className="role-name">{role.name}</h3>
              <span
                className={`trend-badge trend-${role.demand_trend}`}
                style={{ backgroundColor: getTrendColor(role.demand_trend) + '20', color: getTrendColor(role.demand_trend) }}
              >
                {role.demand_trend}
              </span>
            </div>
            <div className="role-skills">
              <p className="skills-label">Required Skills:</p>
              <div className="skills-tags">
                {role.required_skills.map((skill, index) => (
                  <span key={index} className="skill-tag">
                    {skill}
                  </span>
                ))}
              </div>
            </div>
            <p className="role-updated">
              Last updated: {new Date(role.last_updated).toLocaleDateString()}
            </p>
          </Card>
        ))}
      </div>
    </div>
  )
}

export default RoleTrends

