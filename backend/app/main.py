from fastapi import FastAPI
from app.clients.nvd_client import get_cve_details
from app.clients.virustotal_client import check_file_hash
from app.clients.abuseipdb_client import check_ip_reputation

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "LURK API is running"}

@app.get("/cve/{cve_id}")
async def cve_lookup(cve_id: str):
    return await get_cve_details(cve_id)

@app.get("/hash/{file_hash}")
async def hash_lookup(file_hash: str):
    return await check_file_hash(file_hash)

@app.get("/ip/{ip_address}")
async def ip_lookup(ip_address: str):
    return await check_ip_reputation(ip_address)