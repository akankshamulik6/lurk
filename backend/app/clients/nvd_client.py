import httpx
from app.config import NVD_API_KEY

BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

async def get_cve_details(cve_id: str) -> dict:
    headers = {"apiKey": NVD_API_KEY} if NVD_API_KEY else {}
    params = {"cveId": cve_id}

    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

    if not data.get("vulnerabilities"):
        return {"error": f"No data found for {cve_id}"}

    vuln = data["vulnerabilities"][0]["cve"]
    return {
        "id": vuln["id"],
        "description": vuln["descriptions"][0]["value"],
        "published": vuln["published"],
        "cvss": _extract_cvss(vuln),
    }

def _extract_cvss(vuln: dict) -> dict:
    metrics = vuln.get("metrics", {})
    for version_key in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
        if version_key in metrics:
            m = metrics[version_key][0]["cvssData"]
            return {"score": m.get("baseScore"), "severity": m.get("baseSeverity")}
    return {"score": None, "severity": "UNKNOWN"}