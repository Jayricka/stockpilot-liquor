import { ArrowRight } from 'lucide-react'

function Pricing() {
  return (
    <section className="section pricing-section" id="pricing">
      <div className="pricing-card">
        <div>
          <div className="section-label">Pricing</div>

          <h2>Plans designed for growing businesses.</h2>

          <p>
            Proposed pricing will be confirmed as the product moves
            through customer discovery and pilot testing.
          </p>
        </div>

        <a className="button button-primary" href="#contact">
          Discuss your needs
          <ArrowRight size={17} />
        </a>
      </div>
    </section>
  )
}

export default Pricing
