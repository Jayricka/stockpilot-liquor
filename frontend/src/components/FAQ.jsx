import { ChevronDown } from 'lucide-react'

const questions = [
  {
    question: 'Who is StockPilot for?',
    answer:
      'StockPilot is being designed for licensed liquor-store owners, managers, and staff who need clearer business records.',
  },
  {
    question: 'Can I use StockPilot on my phone?',
    answer:
      'The frontend is being designed responsively for desktop, tablet, and mobile use.',
  },
  {
    question: 'Does StockPilot support M-Pesa?',
    answer:
      'M-Pesa is supported as a payment method in the current backend. Direct M-Pesa API integration is planned for a later phase.',
  },
  {
    question: 'Is pricing confirmed?',
    answer:
      'Not yet. Pricing will be confirmed after pilot feedback and customer discovery.',
  },
]

function FAQ() {
  return (
    <section className="section faq-section" id="faq">
      <div className="section-heading centered-heading">
        <div>
          <div className="section-label">Questions</div>
          <h2>Frequently asked questions</h2>
        </div>
      </div>

      <div className="faq-list">
        {questions.map((item) => (
          <details key={item.question}>
            <summary>
              <span>{item.question}</span>
              <ChevronDown size={18} />
            </summary>

            <p>{item.answer}</p>
          </details>
        ))}
      </div>
    </section>
  )
}

export default FAQ
