from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.jobs.daily_report import generate_daily_report
from app.db import init_db, SessionLocal
from app.models import ThreatReport
from app.clients.nvd_client import get_cve_details
from app.clients.virustotal_client import check_file_hash
from app.clients.abuseipdb_client import check_ip_reputation
from app.clients.llm_client import summarize_cve
from pydantic import BaseModel
from app.clients.llm_client import run_agent
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
scheduler = AsyncIOScheduler()

@app.on_event("startup")
async def startup():
    init_db()
    scheduler.add_job(generate_daily_report, "cron", hour=6, minute=0)
    scheduler.start()
@app.get("/")
async def root():
    return {"message": "LURK API is running"}

@app.get("/cve/{cve_id}")
async def cve_lookup(cve_id: str):
    return await get_cve_details(cve_id)

@app.get("/hash/{file_hash}")
async def hash_lookup(file_hash: str):
    return await check_file_hash(file_hash)

@app.get("/ip/{ip_address}")
async def ip_lookup(ip_address: str):
    return await check_ip_reputation(ip_address)

@app.get("/cve/{cve_id}/analyze")
async def cve_analyze(cve_id: str):
    raw_data = await get_cve_details(cve_id)
    if "error" in raw_data:
        return raw_data
    analysis = await summarize_cve(raw_data)
    return analysis
class QuestionRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_agent(req: QuestionRequest):
    answer = await run_agent(req.question)
    return {"answer": answer}
@app.get("/reports/latest")
async def latest_report():
    db = SessionLocal()
    report = db.query(ThreatReport).order_by(ThreatReport.id.desc()).first()
    db.close()
    if not report:
        return {"message": "No reports yet"}
    return {"date": report.date, "summary": report.summary}