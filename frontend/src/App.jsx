import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Skills from './pages/Skills'
import SkillDetail from './pages/SkillDetail'
import HighRiskSkills from './pages/HighRiskSkills'
import EmergingSkills from './pages/EmergingSkills'
import RoleTrends from './pages/RoleTrends'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/skills" element={<Skills />} />
        <Route path="/skills/:skillName" element={<SkillDetail />} />
        <Route path="/high-risk" element={<HighRiskSkills />} />
        <Route path="/emerging" element={<EmergingSkills />} />
        <Route path="/roles" element={<RoleTrends />} />
      </Routes>
    </Layout>
  )
}

export default App



