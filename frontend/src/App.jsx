import { useState } from 'react'
import api from './api'
import CveCard from './components/CveCard'

function App() {
  const [cveId, setCveId] = useState('')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSearch = async () => {
    if (!cveId.trim()) return
    setLoading(true)
    setError(null)
    setData(null)

    try {
      const res = await api.get(`/cve/${cveId.trim()}/analyze`)
      if (res.data.error) {
        setError(res.data.error)
      } else {
        setData(res.data)
      }
    } catch (err) {
      setError('Something went wrong. Check the CVE ID and try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSearch()
  }

  return (
    <div className="min-h-screen bg-void text-line p-8">
      <h1 className="text-2xl tracking-widest mb-8">LURK</h1>

      <div className="flex gap-2 mb-8 max-w-2xl">
        <input
          type="text"
          value={cveId}
          onChange={(e) => setCveId(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="ENTER CVE ID (e.g. CVE-2024-3094)"
          className="flex-1 bg-transparent border border-accent/40 px-4 py-2 text-sm tracking-wide placeholder:text-accent/40 focus:outline-none focus:border-accent"
        />
        <button
          onClick={handleSearch}
          className="border border-accent/40 px-4 py-2 text-xs tracking-widest hover:border-accent hover:text-accent transition-colors"
        >
          ANALYZE
        </button>
      </div>

      {loading && (
        <p className="text-xs tracking-widest text-accent/60">LOADING...</p>
      )}

      {error && (
        <p className="text-xs tracking-widest text-critical">{error}</p>
      )}

      {data && <CveCard data={data} />}
    </div>
  )
}

export default App