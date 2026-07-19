import asyncio
from app.clients.nvd_client import get_cve_details

async def main():
    result = await get_cve_details("CVE-2024-3094")
    print(result)

asyncio.run(main())