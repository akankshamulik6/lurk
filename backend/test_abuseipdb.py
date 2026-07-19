import asyncio
from app.clients.abuseipdb_client import check_ip_reputation

async def main():
    result = await check_ip_reputation("118.25.6.39")
    print(result)

asyncio.run(main())