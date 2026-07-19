import asyncio
from app.db import init_db
from app.jobs.daily_report import generate_daily_report

async def main():
    init_db()
    summary = await generate_daily_report()
    print(summary)

asyncio.run(main())