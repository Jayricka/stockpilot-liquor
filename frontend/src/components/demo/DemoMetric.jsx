function DemoMetric({
  icon,
  label,
  value,
}) {
  return (
    <div className="demo-metric">
      <div className="demo-metric-icon">
        {icon}
      </div>

      <div>
        <span>{label}</span>
        <strong>{value}</strong>
      </div>
    </div>
  )
}

export default DemoMetric
