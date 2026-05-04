import '../css/NavBar.css'
import { useAuth } from '../context/AuthContext'

import { Link } from 'react-router-dom'
import { useNavigate } from 'react-router-dom'

function NavBar() {
  const { isAuthenticated, user, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate('/login')
  }

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link to="/">AuguSTREMIo</Link>
      </div>
      <div className="navbar-links">
        <Link to="/" className="nav-link">
          Home
        </Link>
        <Link to="/favorites" className="nav-link">
          Favorites
        </Link>
        <div className="navbar-links">
          {isAuthenticated ? (
            <>
              <span>{user?.email}</span>
              <button type="button" className="nav-link" onClick={handleLogout}>
                Logout
              </button>
            </>
          ) : (
            <Link className="nav-link" to="/login">
              Login
            </Link>
          )}
        </div>
      </div>
    </nav>
  )
}

export default NavBar
