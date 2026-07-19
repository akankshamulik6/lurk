import asyncio
from app.clients.virustotal_client import check_file_hash

async def main():
    result = await check_file_hash("44d88612fea8a8f36de82e1278abb02f")
    print(result)

asyncio.run(main())