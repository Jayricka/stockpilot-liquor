import { Menu, X, Zap } from 'lucide-react'
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
        <a className="brand" href="#top">
          <span className="brand-mark">
            <Zap size={18} strokeWidth={2.5} />
          </span>

          <span>
            <strong>StockPilot</strong>
            <small>Liquor business management</small>
          </span>
        </a>

        <nav className={`nav-links ${menuOpen ? 'is-open' : ''}`}>
          <a href="#features" onClick={closeMenu}>
            Features
          </a>

          <a href="#how-it-works" onClick={closeMenu}>
            How it works
          </a>

          <a href="#why-stockpilot" onClick={closeMenu}>
            Why StockPilot
          </a>

          <a href="#pricing" onClick={closeMenu}>
            Pricing
          </a>

          <a href="#faq" onClick={closeMenu}>
            FAQ
          </a>

          <a className="nav-login" href="#contact" onClick={closeMenu}>
            Request a demo
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
        >
          {menuOpen ? <X size={22} /> : <Menu size={22} />}
        </button>
      </header>
    </>
  )
}

export default Navbar
