/* eslint-disable react-refresh/only-export-components */

import {
  createContext,
  useContext,
  useMemo,
  useState,
} from 'react'

const AuthContext = createContext(null)

function getStoredUser() {
  const storedUser = localStorage.getItem(
    'stocksafi-user',
  )

  if (!storedUser) {
    return null
  }

  try {
    return JSON.parse(storedUser)
  } catch {
    localStorage.removeItem('stocksafi-user')
    return null
  }
}

function clearSessionState() {
  localStorage.removeItem('stocksafi-access')
  localStorage.removeItem('stocksafi-refresh')
  localStorage.removeItem('stocksafi-user')

  sessionStorage.removeItem(
    'stocksafi-business',
  )

  sessionStorage.removeItem(
    'stocksafi-subscription',
  )
}

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(
    () => localStorage.getItem('stocksafi-access'),
  )

  const [user, setUser] = useState(getStoredUser)

  function saveSession(tokens, userData = null) {
    sessionStorage.removeItem(
      'stocksafi-business',
    )

    sessionStorage.removeItem(
      'stocksafi-subscription',
    )

    localStorage.setItem(
      'stocksafi-access',
      tokens.access,
    )

    if (tokens.refresh) {
      localStorage.setItem(
        'stocksafi-refresh',
        tokens.refresh,
      )
    }

    setAccessToken(tokens.access)

    if (userData) {
      localStorage.setItem(
        'stocksafi-user',
        JSON.stringify(userData),
      )

      setUser(userData)
    }
  }

  function logout() {
    clearSessionState()

    setAccessToken(null)
    setUser(null)
  }

  const value = useMemo(
    () => ({
      accessToken,
      user,
      isAuthenticated: Boolean(accessToken),
      saveSession,
      logout,
    }),
    [accessToken, user],
  )

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)

  if (!context) {
    throw new Error(
      'useAuth must be used inside an AuthProvider',
    )
  }

  return context
}
