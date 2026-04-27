import '../css/Home.css'

import MovieCard from '../components/MovieCard'
import { searchMovies, getPopularMovies } from '../services/api'
import { useState, useEffect } from 'react'

function Home() {
  const [searchQuery, setSearchQuery] = useState('')
  const [movies, setMovies] = useState([])
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  // Load movies when loads the page, so rendering stays clean and avoids repeated API calls.
  useEffect(() => {
    const loadPopularMovies = async () => {
      try {
        const popularMovies = await getPopularMovies()
        setMovies(popularMovies)
      } catch (err) {
        console.log(err)
        setError('Failed to load movies...')
      } finally {
        setLoading(false)
      }
    }
    loadPopularMovies()
  }, []) // This [] is what tells to load only once when starting

  const handleSearch = async (e) => {
    e.preventDefault() // Prevent the form submit from refreshing the page, so React can handle the search.

    if (!searchQuery.trim()) return
    if (loading) return // Not search while previous search not done
    setLoading(true)

    try {
      const searchResults = await searchMovies(searchQuery)
      setMovies(searchResults)
      setError(null)
    } catch (err) {
      console.log(err)
      setError('Failed to search movies...')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="home">
      <form onSubmit={handleSearch} className="search-form">
        <input
          type="text"
          placeholder="Search for movies..."
          className="search-input"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
        <button type="submit" className="search-button">
          Search
        </button>
      </form>

      {error && <div className="error-message">{error}</div>}

      {loading ? (
        <div className="loading"> Loading...</div>
      ) : (
        <div className="movies-grid">
          {movies.map(
            (movie) =>
              movie.title.toLowerCase().startsWith(searchQuery.toLocaleLowerCase()) && (
                <MovieCard movie={movie} key={movie.id} />
              ),
          )}
        </div>
      )}
    </div>
  )
}

export default Home
