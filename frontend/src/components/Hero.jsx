import {
  ArrowRight,
  Check,
  CircleDollarSign,
} from 'lucide-react'

import DashboardPreview from './DashboardPreview'

function Hero() {
  return (
    <section className="hero-section" id="top">
      <div className="hero-copy">
        <div className="eyebrow">
          <span className="eyebrow-icon">
            <CircleDollarSign size={15} />
          </span>

          One place for your business
        </div>

        <h1>
          Run your liquor store with{' '}
          <span>clarity and control.</span>
        </h1>

        <p>
          StockPilot brings inventory, sales, purchases, suppliers,
          deliveries, and business insights into one simple platform
          built for modern liquor-store owners.
        </p>

        <div className="hero-actions">
          <a className="button button-primary" href="#/demo">
            Get started
            <ArrowRight size={17} />
          </a>

          <a className="button button-secondary" href="#product-preview">
            Explore the product
          </a>
        </div>

        <div className="hero-note">
          <Check size={16} />
          Designed for desktop and mobile workflows
        </div>
      </div>

      <DashboardPreview />
    </section>
  )
}

export default Hero
