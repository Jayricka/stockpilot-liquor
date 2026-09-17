function WhyStockPilot() {
  return (
    <section className="section split-section" id="why-stockpilot">
      <div className="section-heading compact-heading">
        <div>
          <div className="section-label">
            Built around your workflow
          </div>

          <h2>
            Your store is busy enough. Your systems should be simple.
          </h2>
        </div>

        <p>
          StockPilot is designed to help business owners spend less
          time searching through records and more time understanding
          what is happening in their stores.
        </p>
      </div>

      <div className="benefit-panel">
        <Benefit
          number="01"
          title="Clear daily activity"
          description="See sales, purchases, stock levels, and deliveries from one workspace."
        />

        <Benefit
          number="02"
          title="Practical business decisions"
          description="Use organized records and reports to understand your operation."
        />

        <Benefit
          number="03"
          title="Ready to grow with you"
          description="Start with essential workflows and expand as your business needs evolve."
        />
      </div>
    </section>
  )
}

function Benefit({ number, title, description }) {
  return (
    <div className="benefit-row">
      <div className="benefit-number">{number}</div>

      <div>
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  )
}

export default WhyStockPilot
