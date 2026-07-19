from fastapi import FastAPI
from app.clients.nvd_client import get_cve_details

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "LURK API is running"}

@app.get("/cve/{cve_id}")
async def cve_lookup(cve_id: str):
    return await get_cve_details(cve_id)