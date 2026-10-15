import {
  ArrowRight,
  Menu,
  Play,
  X,
  Zap,
} from 'lucide-react'
import { useState } from 'react'
import { useTheme } from '../context/ThemeContext.jsx'

function Navbar() {
  const [menuOpen, setMenuOpen] = useState(false)
  const { isDark, toggleTheme } = useTheme()

  const closeMenu = () => setMenuOpen(false)

  return (
    <>
      <div className="announcement">
        <span className="announcement-dot" />
        Built for modern liquor-store operations
      </div>

      <header className="navbar">
        <a className="brand" href="#top" onClick={closeMenu}>
          <span className="brand-mark">
            <Zap size={18} strokeWidth={2.5} />
          </span>

          <span>
            <strong>StockSafi</strong>
            <small>Liquor business management</small>
          </span>
        </a>

        <nav
          id="primary-navigation"
          className={`nav-links ${menuOpen ? 'is-open' : ''}`}
        >
          <a href="#features" onClick={closeMenu}>
            Features
          </a>
          <a href="#how-it-works" onClick={closeMenu}>
            How it works
          </a>
          <a href="#why-stocksafi" onClick={closeMenu}>
            Why StockSafi
          </a>
          <a href="#pricing" onClick={closeMenu}>
            Pricing
          </a>
          <a href="#faq" onClick={closeMenu}>
            FAQ
          </a>

          <a
            className="nav-login"
            href="/login"
            onClick={closeMenu}
          >
            Login
          </a>

          <a
            className="nav-register"
            href="/register"
            onClick={closeMenu}
          >
            Get started <ArrowRight size={14} />
          </a>

          <button
            className="theme-toggle"
            type="button"
            onClick={toggleTheme}
            aria-label="Toggle theme"
            title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {isDark ? '☀' : '☾'}
          </button>
        </nav>

        <button
          className="mobile-menu-button"
          type="button"
          onClick={() => setMenuOpen((open) => !open)}
          aria-label={menuOpen ? 'Close menu' : 'Open menu'}
          aria-expanded={menuOpen}
          aria-controls="primary-navigation"
        >
          {menuOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </header>

      <a className="floating-demo-cta" href="/demo">
        <span className="floating-demo-icon">
          <Play size={15} fill="currentColor" />
        </span>
        <span>Try the demo</span>
        <ArrowRight className="floating-demo-arrow" size={16} />
      </a>
    </>
  )
}

export default Navbar
