import { Navigate, Outlet } from 'react-router-dom'

import { useAuth } from '../../context/AuthContext.jsx'
import Sidebar from './Sidebar'
import Topbar from './Topbar'

function AppLayout() {
  const { isAuthenticated } = useAuth()

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }

  return (
    <div className="app-shell">
      <Sidebar />

      <div className="app-main">
        <Topbar />

        <main className="app-content">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

export default AppLayout
