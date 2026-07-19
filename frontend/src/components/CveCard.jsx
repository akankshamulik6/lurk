function CveCard({ data }) {
  if (!data) return null

  const severityColor = {
    CRITICAL: "text-critical border-critical",
    HIGH: "text-high border-high",
    MEDIUM: "text-medium border-medium",
    LOW: "text-low border-low",
  }[data.severity] || "text-line border-line"

  return (
    <div className="border border-accent/40 p-6 max-w-2xl">
      <div className="flex justify-between items-center border-b border-accent/40 pb-3 mb-4">
        <span className="text-xs tracking-widest text-accent">CVE DOSSIER</span>
        <span className="text-xs tracking-widest text-accent">{data.cve_id}</span>
      </div>

      <div className="space-y-3 text-sm">
        <Row label="CVSS SCORE" value={data.cvss_score ?? "UNKNOWN"} />
        <Row 
          label="SEVERITY" 
          value={data.severity} 
          valueClass={`px-2 py-0.5 border ${severityColor}`} 
        />
        <Row label="EXPLOITATION" value={data.exploitation_status} />
        
        <div className="pt-3 border-t border-accent/20">
          <div className="text-xs tracking-widest text-accent mb-1">SUMMARY</div>
          <p className="text-line/90 leading-relaxed">{data.plain_summary}</p>
        </div>

        <div className="pt-3 border-t border-accent/20">
          <div className="text-xs tracking-widest text-accent mb-1">MITIGATION</div>
          <p className="text-line/90 leading-relaxed">{data.mitigation}</p>
        </div>
      </div>
    </div>
  )
}

function Row({ label, value, valueClass = "" }) {
  return (
    <div className="flex justify-between items-center">
      <span className="text-xs tracking-widest text-accent">{label}</span>
      <span className={`text-sm ${valueClass}`}>{value}</span>
    </div>
  )
}

export default CveCard