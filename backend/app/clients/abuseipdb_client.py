import httpx
from app.config import ABUSEIPDB_API_KEY

BASE_URL = "https://api.abuseipdb.com/api/v2/check"

async def check_ip_reputation(ip: str) -> dict:
    headers = {"Key": ABUSEIPDB_API_KEY, "Accept": "application/json"} if ABUSEIPDB_API_KEY else {}
    params = {"ipAddress": ip}

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

    attrs = data.get("data", {})

    return {
        "ip": attrs.get("ipAddress"),
        "abuse_confidence_score": attrs.get("abuseConfidenceScore"),
        "total_reports": attrs.get("totalReports"),
        "is_tor": attrs.get("isTor"),
        "usage_type": attrs.get("usageType"),
        "country_code": attrs.get("countryCode"),
        "isp": attrs.get("isp"),
        "last_reported_at": attrs.get("lastReportedAt"),
    }