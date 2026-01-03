import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import Card from '../components/Card'
import SkillCard from '../components/SkillCard'
import Loading from '../components/Loading'
import Error from '../components/Error'
import {
  getHighRiskSkills,
  getEmergingSkills,
  getSkills,
  healthCheck,
  triggerPipeline,
} from '../services/api'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import './Dashboard.css'

const Dashboard = () => {
  const [stats, setStats] = useState(null)
  const [highRiskSkills, setHighRiskSkills] = useState([])
  const [emergingSkills, setEmergingSkills] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [health, setHealth] = useState(null)
  const [pipelineRunning, setPipelineRunning] = useState(false)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      setLoading(true)
      setError(null)

      // Check API health
      const healthData = await healthCheck()
      setHealth(healthData)

      // Load data in parallel
      const [highRisk, emerging, allSkills] = await Promise.all([
        getHighRiskSkills(5),
        getEmergingSkills(5),
        getSkills({ limit: 100 }),
      ])

      setHighRiskSkills(highRisk)
      setEmergingSkills(emerging)

      // Calculate stats
      const totalSkills = allSkills.length
      const highRiskCount = allSkills.filter((s) => s.risk_score >= 0.7).length
      const lowRiskCount = allSkills.filter((s) => s.risk_score <= 0.3).length
      const avgRisk =
        totalSkills > 0
          ? allSkills.reduce((sum, s) => sum + s.risk_score, 0) / totalSkills
          : 0

      setStats({
        totalSkills,
        highRiskCount,
        lowRiskCount,
        avgRisk,
        chartData: allSkills.slice(0, 10).map((skill) => ({
          name: skill.name,
          current: skill.current_demand,
          forecast: skill.forecast_demand,
          risk: (skill.risk_score * 100).toFixed(0),
        })),
      })
    } catch (err) {
      console.error('Dashboard load error:', err)
      setError(err.message || 'Failed to load dashboard data')
    } finally {
      setLoading(false)
    }
  }

  const handleRunPipeline = async () => {
  try {
    setPipelineRunning(true)
    await triggerPipeline() // triggers pipeline, returns immediately

    // Poll every 2 seconds until new data is available
    const interval = setInterval(async () => {
      const emerging = await getEmergingSkills(5)
      const highRisk = await getHighRiskSkills(5)

      setEmergingSkills(emerging)
      setHighRiskSkills(highRisk)

      // Stop polling if new data appears
      if (emerging.length > 0 || highRisk.length > 0) {
        clearInterval(interval)
        setPipelineRunning(false)
      }
    }, 2000)
  } catch (err) {
    console.error(err)
    setPipelineRunning(false)
  }
}


  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="header-content">
          <h1>Skill Obsolescence Dashboard</h1>
          <p className="dashboard-subtitle">
            Monitor technology trends and predict skill demand with AI-powered insights
          </p>
        </div>

        <div className="header-actions">
          {health && (
            <div className="health-status">
              <span
                className={`status-indicator ${
                  health.status === 'healthy' ? 'online' : 'offline'
                }`}
              ></span>
              <span>API {health.status === 'healthy' ? 'Online' : 'Offline'}</span>
            </div>
          )}

          <button
            className="pipeline-btn"
            onClick={handleRunPipeline}
            disabled={pipelineRunning}
          >
            {pipelineRunning ? 'Running Pipeline…' : 'Run Pipeline'}
          </button>
        </div>
      </div>

      {(loading || pipelineRunning) && <Loading message="Fetching latest skills..." />}

      {error && <Error message={error} onRetry={loadDashboardData} />}

      {stats && (
        <>
          <div className="stats-grid">
            <Card className="stat-card">
              <div className="stat-content">
                <div className="stat-icon">📊</div>
                <div>
                  <div className="stat-value">{stats.totalSkills}</div>
                  <div className="stat-label">Total Skills Tracked</div>
                </div>
              </div>
            </Card>
            <Card className="stat-card">
              <div className="stat-content">
                <div className="stat-icon">⚠️</div>
                <div>
                  <div className="stat-value">{stats.highRiskCount}</div>
                  <div className="stat-label">High Risk Skills</div>
                </div>
              </div>
            </Card>
            <Card className="stat-card">
              <div className="stat-content">
                <div className="stat-icon">✨</div>
                <div>
                  <div className="stat-value">{stats.lowRiskCount}</div>
                  <div className="stat-label">Low Risk Skills</div>
                </div>
              </div>
            </Card>
            <Card className="stat-card">
              <div className="stat-content">
                <div className="stat-icon">📈</div>
                <div>
                  <div className="stat-value">{(stats.avgRisk * 100).toFixed(1)}%</div>
                  <div className="stat-label">Average Risk Score</div>
                </div>
              </div>
            </Card>
          </div>

          <div className="dashboard-charts">
            <Card title="Demand Forecast" subtitle="Current vs Forecasted Demand">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={stats.chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="current" fill="#6366f1" name="Current Demand" />
                  <Bar dataKey="forecast" fill="#8b5cf6" name="Forecasted Demand" />
                </BarChart>
              </ResponsiveContainer>
            </Card>

            <Card title="Risk Distribution" subtitle="Risk scores by skill">
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={stats.chartData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="risk" fill="#ef4444" name="Risk Score %" />
                </BarChart>
              </ResponsiveContainer>
            </Card>
          </div>
        </>
      )}

      <div className="dashboard-sections">
        <div className="dashboard-section">
          <div className="section-header">
            <h2>High Risk Skills</h2>
            <Link to="/high-risk" className="view-all-link">
              View All →
            </Link>
          </div>
          <div className="skills-grid">
            {highRiskSkills.length > 0 ? (
              highRiskSkills.map((skill) => <SkillCard key={skill.name} skill={skill} />)
            ) : (
              <p className="empty-state">No high-risk skills found</p>
            )}
          </div>
        </div>

        <div className="dashboard-section">
          <div className="section-header">
            <h2>Emerging Skills</h2>
            <Link to="/emerging" className="view-all-link">
              View All →
            </Link>
          </div>
          <div className="skills-grid">
            {emergingSkills.length > 0 ? (
              emergingSkills.map((skill) => <SkillCard key={skill.name} skill={skill} />)
            ) : (
              <p className="empty-state">No emerging skills found</p>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
