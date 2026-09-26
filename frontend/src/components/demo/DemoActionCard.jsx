import {
  ArrowRight,
  Loader2,
} from 'lucide-react'

function DemoActionCard({
  title,
  description,
  icon,
  products,
  selectedProduct,
  quantity,
  onProductChange,
  onQuantityChange,
  onSubmit,
  loading,
  buttonLabel,
}) {
  return (
    <article className="demo-action-card">
      <div className="demo-action-heading">
        <div className="demo-action-icon">
          {icon}
        </div>

        <div>
          <h2>{title}</h2>
          <p>{description}</p>
        </div>
      </div>

      <label>
        Product

        <select
          value={selectedProduct}
          onChange={(event) =>
            onProductChange(
              event.target.value,
            )
          }
        >
          {products.map((product) => (
            <option
              value={product.id}
              key={product.id}
            >
              {product.name}
            </option>
          ))}
        </select>
      </label>

      <label>
        Quantity

        <input
          type="number"
          min="1"
          step="1"
          value={quantity}
          onChange={(event) =>
            onQuantityChange(
              event.target.value,
            )
          }
        />
      </label>

      <button
        className="button button-primary"
        type="button"
        onClick={onSubmit}
        disabled={loading}
      >
        {loading ? (
          <>
            Processing
            <Loader2
              size={16}
              className="demo-spin"
            />
          </>
        ) : (
          <>
            {buttonLabel}
            <ArrowRight size={16} />
          </>
        )}
      </button>
    </article>
  )
}

export default DemoActionCard
