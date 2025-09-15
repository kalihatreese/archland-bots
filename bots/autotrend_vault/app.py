from fastapi import FastAPI, Query
from datetime import date
from typing import List, Dict

app = FastAPI()

@app.get("/health")
def health(): return {"ok": True}

@app.get("/hot")
def hot(limit: int = Query(50, ge=1, le=200), date: date | None = None) -> Dict:
    items: List[Dict] = [
        {"sku": f"SKU{i:04d}", "title": f"Item {i}", "units": 100 - i}
        for i in range(limit)
    ]
    return {"date": str(date) if date else "unspecified", "limit": limit, "items": items}
