import { ArrowRight } from 'lucide-react'

function ContactCTA() {
  return (
    <section className="contact-section" id="contact">
      <div>
        <div className="section-label">Let's talk</div>

        <h2>Ready to bring more control to your store?</h2>

        <p>
          Request a product walkthrough and help shape the next
          stage of StockPilot.
        </p>
      </div>

      <a
        className="button button-light"
        href="mailto:hello@stockpilot.example"
      >
        Request a demo
        <ArrowRight size={17} />
      </a>
    </section>
  )
}

export default ContactCTA
