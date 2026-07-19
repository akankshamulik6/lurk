import httpx
from app.config import VT_API_KEY

BASE_URL = "https://www.virustotal.com/api/v3/files"

async def check_file_hash(file_hash: str) -> dict:
    headers = {"x-apikey": VT_API_KEY} if VT_API_KEY else {}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/{file_hash}", headers=headers, timeout=15)

        if response.status_code == 404:
            return {"error": f"No data found for hash {file_hash}"}

        response.raise_for_status()
        data = response.json()

    attrs = data["data"]["attributes"]
    stats = attrs.get("last_analysis_stats", {})

    return {
        "hash": file_hash,
        "malicious_count": stats.get("malicious", 0),
        "harmless_count": stats.get("harmless", 0),
        "suspicious_count": stats.get("suspicious", 0),
        "reputation": attrs.get("reputation"),
        "threat_label": attrs.get("popular_threat_classification", {}).get("suggested_threat_label", "unknown"),
        "last_analysis_date": attrs.get("last_analysis_date"),
    }