import { useState, useEffect } from 'react'
import api from './api'
import CveCard from './components/CveCard'
import DailyReport from './components/DailyReport'
import LookupCard from './components/LookupCard'

function App() {
  const [cveId, setCveId] = useState('')
  const [cveData, setCveData] = useState(null)
  const [cveLoading, setCveLoading] = useState(false)
  const [cveError, setCveError] = useState(null)

  const [ip, setIp] = useState('')
  const [ipData, setIpData] = useState(null)
  const [ipLoading, setIpLoading] = useState(false)

  const [hash, setHash] = useState('')
  const [hashData, setHashData] = useState(null)
  const [hashLoading, setHashLoading] = useState(false)

  const [report, setReport] = useState(null)

  useEffect(() => {
    api.get('/reports/latest')
      .then(res => setReport(res.data))
      .catch(() => setReport(null))
  }, [])

  const searchCve = async () => {
    if (!cveId.trim()) return
    setCveLoading(true)
    setCveError(null)
    setCveData(null)
    try {
      const res = await api.get(`/cve/${cveId.trim()}/analyze`)
      if (res.data.error) setCveError(res.data.error)
      else setCveData(res.data)
    } catch {
      setCveError('Something went wrong. Check the CVE ID and try again.')
    } finally {
      setCveLoading(false)
    }
  }

  const searchIp = async () => {
    if (!ip.trim()) return
    setIpLoading(true)
    setIpData(null)
    try {
      const res = await api.get(`/ip/${ip.trim()}`)
      setIpData(res.data)
    } catch {
      setIpData({ error: 'Something went wrong checking that IP.' })
    } finally {
      setIpLoading(false)
    }
  }

  const searchHash = async () => {
    if (!hash.trim()) return
    setHashLoading(true)
    setHashData(null)
    try {
      const res = await api.get(`/hash/${hash.trim()}`)
      setHashData(res.data)
    } catch {
      setHashData({ error: 'Something went wrong checking that hash.' })
    } finally {
      setHashLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-void text-line p-8">
      <h1 className="text-2xl tracking-widest mb-8">LURK</h1>

      <DailyReport report={report} />

      {/* CVE Lookup */}
      <div className="flex gap-2 mb-2 max-w-2xl">
        <input
          type="text"
          value={cveId}
          onChange={(e) => setCveId(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && searchCve()}
          placeholder="ENTER CVE ID (e.g. CVE-2024-3094)"
          className="flex-1 bg-transparent border border-accent/40 px-4 py-2 text-sm tracking-wide placeholder:text-accent/40 focus:outline-none focus:border-accent"
        />
        <button onClick={searchCve} className="border border-accent/40 px-4 py-2 text-xs tracking-widest hover:border-accent hover:text-accent transition-colors">
          ANALYZE
        </button>
      </div>
      {cveLoading && <p className="text-xs tracking-widest text-accent/60 mb-4">LOADING...</p>}
      {cveError && <p className="text-xs tracking-widest text-critical mb-4">{cveError}</p>}
      {cveData && <CveCard data={cveData} />}

      {/* IP Lookup */}
      <div className="flex gap-2 mb-2 max-w-2xl mt-4">
        <input
          type="text"
          value={ip}
          onChange={(e) => setIp(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && searchIp()}
          placeholder="ENTER IP ADDRESS"
          className="flex-1 bg-transparent border border-accent/40 px-4 py-2 text-sm tracking-wide placeholder:text-accent/40 focus:outline-none focus:border-accent"
        />
        <button onClick={searchIp} className="border border-accent/40 px-4 py-2 text-xs tracking-widest hover:border-accent hover:text-accent transition-colors">
          CHECK IP
        </button>
      </div>
      {ipLoading && <p className="text-xs tracking-widest text-accent/60 mb-4">LOADING...</p>}
      {ipData && <LookupCard title="IP REPUTATION" data={ipData} />}

      {/* Hash Lookup */}
      <div className="flex gap-2 mb-2 max-w-2xl mt-4">
        <input
          type="text"
          value={hash}
          onChange={(e) => setHash(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && searchHash()}
          placeholder="ENTER FILE HASH (MD5/SHA1/SHA256)"
          className="flex-1 bg-transparent border border-accent/40 px-4 py-2 text-sm tracking-wide placeholder:text-accent/40 focus:outline-none focus:border-accent"
        />
        <button onClick={searchHash} className="border border-accent/40 px-4 py-2 text-xs tracking-widest hover:border-accent hover:text-accent transition-colors">
          CHECK HASH
        </button>
      </div>
      {hashLoading && <p className="text-xs tracking-widest text-accent/60 mb-4">LOADING...</p>}
      {hashData && <LookupCard title="FILE HASH REPUTATION" data={hashData} />}
    </div>
  )
}

export default App