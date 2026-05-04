// src/services/authService.js

import { API_URL, apiFetch } from './api'

export async function loginUser(email, password) {
  const response = await fetch(`${API_URL}/auth/login`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      email,
      password,
    }),
  })

  if (!response.ok) {
    throw new Error('Invalid email or password')
  }

  return response.json()
}

export async function getCurrentUser() {
  const response = await apiFetch('/users/me')

  if (!response.ok) {
    throw new Error('Could not get current user')
  }

  return response.json()
}

export async function registerUser(email, password) {
  const response = await apiFetch('/auth/register', {
    method: 'POST',
    body: JSON.stringify({
      email,
      password,
    }),
  })

  return response.json()
}
