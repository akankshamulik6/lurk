import httpx
from datetime import datetime, timedelta

from app.config import NVD_API_KEY

BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"


async def get_cve_details(cve_id: str) -> dict:
    """
    Fetch details for a single CVE by its ID.
    """

    headers = {"apiKey": NVD_API_KEY} if NVD_API_KEY else {}
    params = {"cveId": cve_id}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=15,
        )
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


async def get_recent_cves(hours: int = 24) -> list[dict]:
    """
    Fetch CVEs published in the last `hours` hours.
    """

    end = datetime.utcnow()
    start = end - timedelta(hours=hours)

    params = {
        "pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "pubEndDate": end.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "resultsPerPage": 20,
    }

    headers = {"apiKey": NVD_API_KEY} if NVD_API_KEY else {}

    async with httpx.AsyncClient() as client:
        response = await client.get(
            BASE_URL,
            headers=headers,
            params=params,
            timeout=20,
        )
        response.raise_for_status()
        data = response.json()

    cves = []

    for item in data.get("vulnerabilities", []):
        vuln = item["cve"]

        cves.append(
            {
                "id": vuln["id"],
                "description": vuln["descriptions"][0]["value"],
                "published": vuln["published"],
                "cvss": _extract_cvss(vuln),
            }
        )

    return cves


def _extract_cvss(vuln: dict) -> dict:
    """
    Extract CVSS score and severity from the vulnerability.
    Supports CVSS v3.1, v3.0 and v2.
    """

    metrics = vuln.get("metrics", {})

    for version_key in [
        "cvssMetricV31",
        "cvssMetricV30",
        "cvssMetricV2",
    ]:
        if version_key in metrics:
            cvss = metrics[version_key][0]["cvssData"]

            return {
                "score": cvss.get("baseScore"),
                "severity": cvss.get("baseSeverity"),
            }

    return {
        "score": None,
        "severity": "UNKNOWN",
    }