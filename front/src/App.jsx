import './css/App.css'

import MovieCard from './components/MovieCard'
import Home from './pages/Home'
import Favorite from './pages/Favorites'
import NavBar from './components/NavBar'
import { MovieProvider } from './context/MovieContext.jsx'
import Login from './pages/Login.jsx'
import { Routes, Route } from 'react-router-dom'
import ProtectedRoute from './components/ProtectedRoute.jsx'
import Signup from './pages/SignUp.jsx'
import { CopilotSidebar } from '@copilotkit/react-ui'

function App() {
  return (
    <MovieProvider>
      <CopilotSidebar />
      <div>
        <NavBar />
      </div>
      <main className="main-content">
        <Routes>
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<Home />} />
            <Route path="/favorites" element={<Favorite />} />
          </Route>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
        </Routes>
      </main>
    </MovieProvider>
  )
}

export default App
