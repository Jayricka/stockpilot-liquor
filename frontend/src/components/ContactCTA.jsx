import { ArrowRight } from 'lucide-react'

function ContactCTA() {
  return (
    <section
      className="contact-section"
      id="contact"
    >
      <div>
        <div className="section-label">
          See it in action
        </div>

        <h2>
          Ready to bring more control to your store?
        </h2>

        <p>
          Explore a working StockPilot workspace
          with no signup, payment, or setup required.
        </p>
      </div>

      <a
        className="button button-light"
        href="/demo"
      >
        Try the interactive demo
        <ArrowRight size={17} />
      </a>
    </section>
  )
}

export default ContactCTA
