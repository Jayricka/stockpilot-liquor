import { Zap } from 'lucide-react'

function Footer() {
  return (
    <footer className="footer">
      <div className="brand footer-brand">
        <span className="brand-mark">
          <Zap size={18} strokeWidth={2.5} />
        </span>

        <span>
          <strong>StockSafi</strong>
          <small>Liquor business management</small>
        </span>
      </div>

      <p>
        © 2026 StockSafi. Built for practical business management.
      </p>
    </footer>
  )
}

export default Footer
