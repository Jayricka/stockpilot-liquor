import {
  ArrowDownRight,
  ArrowUpRight,
  BarChart3,
  Boxes,
  Package,
  Plus,
  ShoppingCart,
  Store,
  Truck,
  TrendingUp,
} from 'lucide-react'

const products = [
  { name: 'Whisky', detail: '12 bottles', price: 'KSh 2,400' },
  { name: 'Vodka', detail: '24 bottles', price: 'KSh 1,800' },
  { name: 'Gin', detail: '08 bottles', price: 'KSh 2,100' },
]

const stockMovements = [
  {
    icon: Truck,
    label: 'Purchase received',
    detail: 'Supplier delivery',
    amount: '+24 units',
    type: 'positive',
  },
  {
    icon: ShoppingCart,
    label: 'Sale recorded',
    detail: 'Customer purchase',
    amount: '-3 units',
    type: 'negative',
  },
]

function ProductPreview() {
  return (
    <div className="workflow-preview">
      <div className="workflow-preview-heading">
        <div className="workflow-preview-title">
          <Package size={16} />
          <span>Product catalogue</span>
        </div>
        <span className="workflow-preview-action">
          <Plus size={13} /> Add
        </span>
      </div>

      <div className="workflow-product-list">
        {products.map((product) => (
          <div className="workflow-product-row" key={product.name}>
            <span className="workflow-product-icon">
              <Package size={17} />
            </span>
            <span className="workflow-product-info">
              <strong>{product.name}</strong>
              <small>{product.detail}</small>
            </span>
            <span className="workflow-product-price">
              {product.price}
            </span>
          </div>
        ))}
      </div>

      <div className="workflow-preview-foot">
        <Store size={14} />
        Your products, organised in one place
      </div>
    </div>
  )
}

function StockPreview() {
  return (
    <div className="workflow-preview">
      <div className="workflow-preview-heading">
        <div className="workflow-preview-title">
          <Boxes size={16} />
          <span>Stock activity</span>
        </div>
        <span className="workflow-status">Live overview</span>
      </div>

      <div className="workflow-stock-total">
        <span>Available stock</span>
        <strong>86 <small>units</small></strong>
        <div className="workflow-stock-track">
          <span />
        </div>
      </div>

      <div className="workflow-movement-list">
        {stockMovements.map((movement) => {
          const Icon = movement.icon

          return (
            <div
              className="workflow-movement-row"
              key={movement.label}
            >
              <span className={`workflow-movement-icon ${movement.type}`}>
                <Icon size={16} />
              </span>
              <span className="workflow-movement-info">
                <strong>{movement.label}</strong>
                <small>{movement.detail}</small>
              </span>
              <strong className={`workflow-movement-amount ${movement.type}`}>
                {movement.amount}
              </strong>
            </div>
          )
        })}
      </div>
    </div>
  )
}

function ReportsPreview() {
  const bars = [32, 48, 38, 68, 54, 82, 64]

  return (
    <div className="workflow-preview">
      <div className="workflow-preview-heading">
        <div className="workflow-preview-title">
          <BarChart3 size={16} />
          <span>Business overview</span>
        </div>
        <span className="workflow-status">This week</span>
      </div>

      <div className="workflow-metrics">
        <div className="workflow-metric">
          <span>Sales recorded</span>
          <strong>KSh 24,850</strong>
          <small><ArrowUpRight size={13} /> Sales total</small>
        </div>
        <div className="workflow-metric">
          <span>Gross profit</span>
          <strong>KSh 6,400</strong>
          <small><TrendingUp size={13} /> Profit overview</small>
        </div>
      </div>

      <div className="workflow-chart">
        <div className="workflow-chart-heading">
          <span>Sales activity</span>
          <span><ArrowDownRight size={13} /> Illustrative</span>
        </div>
        <div className="workflow-chart-bars">
          {bars.map((height, index) => (
            <span key={index} style={{ height: `${height}%` }} />
          ))}
        </div>
        <div className="workflow-chart-labels">
          <span>Mon</span>
          <span>Tue</span>
          <span>Wed</span>
          <span>Thu</span>
          <span>Fri</span>
          <span>Sat</span>
          <span>Sun</span>
        </div>
      </div>
    </div>
  )
}

const stages = [
  {
    number: '01',
    label: 'GET STARTED',
    title: 'Set up your shop',
    description:
      'Create your business workspace, add your products, and organise supplier details.',
    preview: ProductPreview,
  },
  {
    number: '02',
    label: 'RUN YOUR BUSINESS',
    title: 'Manage daily operations',
    description:
      'Record purchases and sales, and follow stock movements as your business operates.',
    preview: StockPreview,
  },
  {
    number: '03',
    label: 'MAKE BETTER DECISIONS',
    title: 'Understand your numbers',
    description:
      'Review sales, gross profit, and stock information to make more informed decisions.',
    preview: ReportsPreview,
  },
]

function HowItWorks() {
  return (
    <section
      className="section workflow-section"
      id="how-it-works"
    >
      <div className="section-heading centered-heading">
        <div>
          <div className="section-label">Simple from day one</div>
          <h2>From your shelves to your sales</h2>
        </div>
        <p>
          One clear workflow to organise your liquor shop,
          keep track of stock, and understand your business.
        </p>
      </div>

      <div className="workflow-grid">
        {stages.map((stage) => {
          const Preview = stage.preview

          return (
            <article className="workflow-card" key={stage.number}>
              <div className="workflow-card-visual">
                <Preview />
              </div>
              <div className="workflow-card-content">
                <span className="workflow-stage-label">
                  <span>{stage.number}</span>
                  {stage.label}
                </span>
                <h3>{stage.title}</h3>
                <p>{stage.description}</p>
              </div>
            </article>
          )
        })}
      </div>

      <p className="workflow-note">
        <span /> Illustrative previews — your actual figures come from
        your business records.
      </p>
    </section>
  )
}

export default HowItWorks
