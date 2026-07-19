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