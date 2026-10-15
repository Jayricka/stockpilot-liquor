import { ChevronDown } from 'lucide-react'

const questions = [
  {
    question: 'Who is StockSafi for?',
    answer:
      'StockSafi is being designed for licensed liquor-store owners, managers, and staff who need clearer business records.',
  },
  {
    question: 'Can I use StockSafi on my phone?',
    answer:
      'The frontend is being designed responsively for desktop, tablet, and mobile use.',
  },
  {
    question: 'Does StockSafi support M-Pesa?',
    answer:
      'M-Pesa is supported as a payment method in the current backend. Direct M-Pesa API integration is planned for a later phase.',
  },
  {
    question: 'Can I try StockSafi before signing up?',
    answer:
      'Yes. You can explore the interactive demo without creating an account. Demo data is isolated from real business workspaces.',
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
