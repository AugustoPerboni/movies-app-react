// src/context/AuthContext.jsx

import { createContext, useContext, useEffect, useState } from 'react'

import { getCurrentUser, loginUser, registerUser } from '../services/authService'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [isLoading, setIsLoading] = useState(true)

  const isAuthenticated = user !== null

  async function loadCurrentUser() {
    const token = localStorage.getItem('access_token')

    if (!token) {
      setUser(null)
      setIsLoading(false)
      return
    }

    try {
      const currentUser = await getCurrentUser()
      setUser(currentUser)
    } catch {
      localStorage.removeItem('access_token')
      setUser(null)
    } finally {
      setIsLoading(false)
    }
  }

  async function login(email, password) {
    const data = await loginUser(email, password)

    localStorage.setItem('access_token', data.access_token)

    const currentUser = await getCurrentUser()
    setUser(currentUser)
  }

  async function register(email, password) {
    await registerUser(email, password)
    await login(email, password)
  }

  function logout() {
    localStorage.removeItem('access_token')
    setUser(null)
  }

  useEffect(() => {
    loadCurrentUser()
  }, [])

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated,
        login,
        register,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider')
  }

  return context
}
