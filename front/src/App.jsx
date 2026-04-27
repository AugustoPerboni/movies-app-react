import './css/App.css'

import MovieCard from './components/MovieCard'
import Home from './pages/Home'
import Favorite from './pages/Favorites'
import NavBar from './components/NavBar'
import { MovieProvider } from './context/MovieContext.jsx'

import { Routes, Route } from 'react-router-dom'

function App() {
  return (
    <MovieProvider>
      <div>
        <NavBar />
      </div>
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/favorites" element={<Favorite />} />
        </Routes>
      </main>
    </MovieProvider>
  )
}

export default App
