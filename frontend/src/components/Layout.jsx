import { Link, useLocation } from 'react-router-dom'
import './Layout.css'

const Layout = ({ children }) => {
  const location = useLocation()

  const isActive = (path) => {
    return location.pathname === path
  }

  return (
    <div className="layout">
      <nav className="navbar">
        <div className="nav-container">
          <Link to="/" className="nav-brand">
            <span className="brand-icon">🔮</span>
            <span className="brand-text">Skill Predictor</span>
          </Link>
          <div className="nav-links">
            <Link
              to="/"
              className={`nav-link ${isActive('/') ? 'active' : ''}`}
            >
              Dashboard
            </Link>
            <Link
              to="/skills"
              className={`nav-link ${isActive('/skills') && location.pathname === '/skills' ? 'active' : ''}`}
            >
              All Skills
            </Link>
            <Link
              to="/high-risk"
              className={`nav-link ${isActive('/high-risk') ? 'active' : ''}`}
            >
              High Risk
            </Link>
            <Link
              to="/emerging"
              className={`nav-link ${isActive('/emerging') ? 'active' : ''}`}
            >
              Emerging
            </Link>
            <Link
              to="/roles"
              className={`nav-link ${isActive('/roles') ? 'active' : ''}`}
            >
              Roles
            </Link>
          </div>
        </div>
      </nav>
      <main className="main-content">
        {children}
      </main>
      <footer className="footer">
        <p>Future Skill & Tech-Stack Obsolescence Predictor © 2024</p>
      </footer>
    </div>
  )
}

export default Layout

