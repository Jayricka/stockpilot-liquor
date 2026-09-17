import { steps } from '../data/landingPage'

function HowItWorks() {
  return (
    <section className="section workflow-section" id="how-it-works">
      <div className="section-heading centered-heading">
        <div>
          <div className="section-label">Simple from day one</div>
          <h2>How StockPilot works</h2>
        </div>

        <p>
          A straightforward workflow for managing the essentials
          of your liquor business.
        </p>
      </div>

      <div className="steps-grid">
        {steps.map((step, index) => (
          <div className="step-card" key={step}>
            <span>{String(index + 1).padStart(2, '0')}</span>
            <h3>{step}</h3>
          </div>
        ))}
      </div>
    </section>
  )
}

export default HowItWorks
