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
    'stockpilot-user',
  )

  if (!storedUser) {
    return null
  }

  try {
    return JSON.parse(storedUser)
  } catch {
    localStorage.removeItem('stockpilot-user')
    return null
  }
}

export function AuthProvider({ children }) {
  const [accessToken, setAccessToken] = useState(
    () => localStorage.getItem('stockpilot-access'),
  )

  const [user, setUser] = useState(getStoredUser)

  function saveSession(tokens, userData = null) {
    localStorage.setItem(
      'stockpilot-access',
      tokens.access,
    )

    if (tokens.refresh) {
      localStorage.setItem(
        'stockpilot-refresh',
        tokens.refresh,
      )
    }

    setAccessToken(tokens.access)

    if (userData) {
      localStorage.setItem(
        'stockpilot-user',
        JSON.stringify(userData),
      )

      setUser(userData)
    }
  }

  function logout() {
    localStorage.removeItem('stockpilot-access')
    localStorage.removeItem('stockpilot-refresh')
    localStorage.removeItem('stockpilot-user')

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
