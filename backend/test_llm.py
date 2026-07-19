import asyncio
from app.clients.nvd_client import get_cve_details
from app.clients.llm_client import summarize_cve

async def main():
    raw_data = await get_cve_details("CVE-2024-3094")
    print("Raw NVD data fetched.")
    analysis = await summarize_cve(raw_data)
    print(analysis)

asyncio.run(main())