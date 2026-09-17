import {
  BarChart3,
  Boxes,
  ClipboardList,
  LayoutDashboard,
  LogOut,
  Package,
  Settings,
  ShoppingCart,
  Truck,
  Users,
  Zap,
} from 'lucide-react'
import { NavLink } from 'react-router-dom'

import { useAuth } from '../../context/AuthContext.jsx'

const navigation = [
  {
    label: 'Overview',
    path: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    label: 'Inventory',
    path: '/inventory',
    icon: Boxes,
  },
  {
    label: 'Products',
    path: '/products',
    icon: Package,
  },
  {
    label: 'Sales',
    path: '/sales',
    icon: ShoppingCart,
  },
  {
    label: 'Purchases',
    path: '/purchases',
    icon: ClipboardList,
  },
  {
    label: 'Suppliers',
    path: '/suppliers',
    icon: Users,
  },
  {
    label: 'Deliveries',
    path: '/deliveries',
    icon: Truck,
  },
  {
    label: 'Reports',
    path: '/reports',
    icon: BarChart3,
  },
]

function Sidebar() {
  const { logout } = useAuth()

  return (
    <aside className="app-sidebar">
      <NavLink className="app-logo" to="/dashboard">
        <span className="brand-mark">
          <Zap size={18} strokeWidth={2.5} />
        </span>

        <span>
          <strong>StockPilot</strong>
          <small>Business management</small>
        </span>
      </NavLink>

      <nav className="sidebar-nav">
        <span className="sidebar-section-title">
          Workspace
        </span>

        {navigation.map((item) => {
          const Icon = item.icon

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `sidebar-link ${
                  isActive ? 'is-active' : ''
                }`
              }
            >
              <Icon size={17} />
              {item.label}
            </NavLink>
          )
        })}
      </nav>

      <div className="sidebar-bottom">
        <NavLink
          className="sidebar-link"
          to="/settings"
        >
          <Settings size={17} />
          Settings
        </NavLink>

        <button
          className="sidebar-link sidebar-logout"
          type="button"
          onClick={logout}
        >
          <LogOut size={17} />
          Sign out
        </button>
      </div>
    </aside>
  )
}

export default Sidebar
