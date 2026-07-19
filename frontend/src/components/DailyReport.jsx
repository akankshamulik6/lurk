function DailyReport({ report }) {
  if (!report) return null

  if (report.message) {
    return (
      <div className="border border-accent/40 p-6 max-w-2xl mb-8">
        <div className="text-xs tracking-widest text-accent mb-2">DAILY THREAT REPORT</div>
        <p className="text-line/60 text-sm">{report.message}</p>
      </div>
    )
  }

  const date = new Date(report.date)
  const formattedDate = date.toLocaleDateString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit'
  })

  return (
    <div className="border border-accent/40 p-6 max-w-2xl mb-8">
      <div className="flex justify-between items-center border-b border-accent/40 pb-3 mb-4">
        <span className="text-xs tracking-widest text-accent">DAILY THREAT REPORT</span>
        <span className="text-xs tracking-widest text-accent/60">{formattedDate}</span>
      </div>
      <p className="text-sm text-line/90 leading-relaxed">{report.summary}</p>
    </div>
  )
}

export default DailyReport