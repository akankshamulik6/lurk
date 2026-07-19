# LURK — Build Notes

## Goal
An AI-powered threat intelligence agent that pulls real-time CVE, IP reputation, 
and file hash data from public security APIs, then uses an LLM to reason over 
that data and generate grounded, plain-English threat summaries.

## MVP Scope (v1)
- [ ] NVD API integration — CVE lookup by ID
- [ ] VirusTotal integration — file hash / URL reputation check
- [ ] Claude API reasoning layer — takes raw API JSON, returns structured summary
- [ ] Basic FastAPI backend with 2-3 working endpoints
- [ ] Simple React chat interface to query the backend
- [ ] Daily automated threat report (APScheduler)

## Future Work (not v1)
- AbuseIPDB integration (IP reputation)
- Shodan integration (exposed device/recon data)
- Multi-turn chat memory
- CVE ↔ IOC correlation engine
- Auth/login for dashboard
- LangChain-based orchestration (skipping for v1, direct Claude tool-use instead)

## Architecture
[Add Excalidraw PNG link here once sketched — save in /docs]

Flow: Frontend (React) → FastAPI backend → LLM layer (Claude) 
↔ API wrappers (NVD, VirusTotal) → DB (SQLite/Postgres)

## Tech Stack
- Backend: FastAPI, Python
- Frontend: React, Tailwind CSS
- DB: SQLite (dev) → Postgres (later)
- LLM: Claude API
- APIs: NVD, VirusTotal (v1) — AbuseIPDB, Shodan (future)

## Daily Log

### 19-07-2026
- Set up GitHub repo, folder structure (backend/frontend/docs)
- Got API keys for NVD, VirusTotal, AbuseIPDB, Shodan
- Set up .env with keys, confirmed .gitignore protecting it
- Next: sketch architecture diagram, then start Phase 1 (FastAPI skeleton + get_cve_details wrapper)

## API Notes

### NVD API
- Endpoint: GET https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={CVE_ID}
- Auth: apiKey header
- Sample test: CVE-2024-3094 (xz-utils backdoor) → returned full CVE data,
  CVSS 3.1 score 10.0 CRITICAL, description, references, affected packages
- Key fields I'll actually use: id, descriptions[0].value, metrics.cvssMetricV31[0].cvssData.baseScore,
  metrics.cvssMetricV31[0].cvssData.baseSeverity, references (for mitigation links)
- Rate limit: 50 requests/30 sec with API key (5 without)
- Notes: response is huge (lots of reference URLs) — I'll need to trim this down 
  before sending to the LLM, only pass the relevant fields

  ### VirusTotal API
- Endpoint: GET https://www.virustotal.com/api/v3/files/{hash}
- Auth: x-apikey header
- Sample test: EICAR test file hash (44d88612fea8a8f36de82e1278abb02f) → returned full 
  analysis: 65/68 engines flagged malicious, reputation score, sandbox verdicts, 
  file type, tags, first/last seen dates
- Key fields I'll actually use: data.attributes.last_analysis_stats (malicious/harmless counts),
  data.attributes.popular_threat_classification.suggested_threat_label,
  data.attributes.reputation, data.attributes.last_analysis_date
- Rate limit: 4 requests/min, 500/day, 15.5K/month (free tier)
- Notes: response is MASSIVE (all 70+ AV engine results) — definitely need to filter 
  down to just last_analysis_stats + threat label before passing to LLM, don't dump 
  raw response into the prompt
  
  ### Shodan API
- Endpoint: GET https://api.shodan.io/shodan/host/{ip}?key={key}
- Auth: key as query param
- Sample test: 8.8.8.8 (Google DNS) → returned org, ISP, open ports, hostnames, 
  geolocation, and per-port banner/service data
- Key fields I'll actually use: ip_str, org, ports, hostnames, data[].port, 
  data[].product (service name), country_name
- Rate limit: 1 request/sec, 100 query credits/month (free tier — quite limited 
  compared to the others)
- Notes: lowest free-tier quota of all four APIs — since this is "future work" 
  not v1, don't worry about optimizing calls yet, but keep in mind for later 
  that Shodan will need aggressive caching once it's actually integrated
### 19-07-2026 (cont.)
- Phase 1 complete: FastAPI backend live with 3 working endpoints
  (/cve/{id}, /hash/{hash}, /ip/{ip})
- All three API wrappers (NVD, VirusTotal, AbuseIPDB) tested standalone 
  before route integration — caught no major issues, all worked first try
- Next: Phase 2 — connect Claude API, build the LLM reasoning layer that 
  takes this raw JSON and returns structured, grounded summaries