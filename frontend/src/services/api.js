/**
 * API service layer for backend communication.
 */
import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000,
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const healthCheck = () => api.get('/health')

export const getSkills = (params = {}) => {
  return api.get('/skills', { params })
}

export const getSkillDetail = (skillName) => {
  return api.get(`/skills/${encodeURIComponent(skillName)}`)
}

export const getHighRiskSkills = (limit = 10) => {
  return api.get('/skills/high-risk', { params: { limit } })
}

export const getEmergingSkills = (limit = 10) => {
  return api.get('/skills/emerging', { params: { limit } })
}

export const getRoleTrends = () => {
  return api.get('/roles/trends')
}

export const triggerPipeline = () => {
  return api.post('/pipeline/run')
}

export const getPipelineStatus = () => {
  return api.get('/pipeline/status')
}

export default api



