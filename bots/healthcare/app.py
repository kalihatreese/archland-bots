from fastapi import FastAPI
import httpx, os

app = FastAPI()

AUTOTREND_URL = os.getenv("AUTOTREND_URL","http://localhost:8090")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/store/hot")
async def store_hot(limit: int = 50, date: str | None = None):
    async with httpx.AsyncClient(timeout=10) as cx:
        r = await cx.get(f"{AUTOTREND_URL}/hot", params={"limit": limit, "date": date})
    return r.json()
