function LookupCard({ title, data }) {
  if (!data) return null

  const entries = Object.entries(data).filter(([key]) => key !== 'error')

  if (data.error) {
    return (
      <div className="border border-critical/40 p-6 max-w-2xl mb-8">
        <div className="text-xs tracking-widest text-critical">{data.error}</div>
      </div>
    )
  }

  return (
    <div className="border border-accent/40 p-6 max-w-2xl mb-8">
      <div className="text-xs tracking-widest text-accent border-b border-accent/40 pb-3 mb-4">
        {title}
      </div>
      <div className="space-y-2 text-sm">
        {entries.map(([key, value]) => (
          <div key={key} className="flex justify-between items-center">
            <span className="text-xs tracking-widest text-accent">
              {key.replace(/_/g, ' ').toUpperCase()}
            </span>
            <span className="text-line/90">{String(value)}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

export default LookupCard