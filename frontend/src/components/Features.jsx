import { ArrowRight } from 'lucide-react'
import { features } from '../data/landingPage'

function Features() {
  return (
    <section className="section" id="features">
      <div className="section-heading">
        <div>
          <div className="section-label">Everything in one place</div>

          <h2>Less manual work. More business visibility.</h2>
        </div>

        <p>
          Bring the essential parts of your liquor-store operation
          together without relying on scattered notebooks and
          spreadsheets.
        </p>
      </div>

      <div className="feature-grid">
        {features.map((feature) => {
          const Icon = feature.icon

          return (
            <article className="feature-card" key={feature.title}>
              <div className="feature-icon">
                <Icon size={21} />
              </div>

              <h3>{feature.title}</h3>

              <p>{feature.description}</p>

              <a href="#contact">
                Learn more
                <ArrowRight size={15} />
              </a>
            </article>
          )
        })}
      </div>
    </section>
  )
}

export default Features
