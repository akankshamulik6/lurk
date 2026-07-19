import json
import httpx
from app.clients.nvd_client import get_recent_cves
from app.config import GROQ_API_KEY
from app.db import SessionLocal
from app.models import ThreatReport

BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

async def generate_daily_report():
    cves = await get_recent_cves(hours=24)
    top_cves = sorted(
        [c for c in cves if c["cvss"]["score"]],
        key=lambda c: c["cvss"]["score"],
        reverse=True,
    )[:5]

    system_prompt = """You are a threat intel analyst. Given a list of today's CVEs,
write a short daily threat report (plain English, 4-6 sentences) highlighting the most
dangerous ones and why. Base this ONLY on the data given — do not invent CVEs."""

    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": json.dumps(top_cves)},
        ],
        "temperature": 0.3,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(BASE_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        result = response.json()
        summary = result["choices"][0]["message"]["content"]

    db = SessionLocal()
    report = ThreatReport(summary=summary, raw_data=json.dumps(top_cves))
    db.add(report)
    db.commit()
    db.close()
    return summary