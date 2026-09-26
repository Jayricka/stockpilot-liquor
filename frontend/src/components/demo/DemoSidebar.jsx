import {
  Package,
  ShieldCheck,
  ShoppingCart,
  TrendingUp,
} from 'lucide-react'

function DemoSidebar({ businessName }) {
  return (
    <aside className="demo-workspace-sidebar">
      <div className="demo-business">
        <small>Business</small>

        <strong>{businessName}</strong>
      </div>

      <nav>
        <div className="demo-nav-link active">
          <TrendingUp size={17} />
          Overview
        </div>

        <div className="demo-nav-link">
          <Package size={17} />
          Products
        </div>

        <div className="demo-nav-link">
          <ShoppingCart size={17} />
          Sales
        </div>
      </nav>

      <div className="demo-sidebar-note">
        <ShieldCheck size={16} />

        <span>
          This workspace uses isolated demo
          data.
        </span>
      </div>
    </aside>
  )
}

export default DemoSidebar
