from fastapi import FastAPI
import os, httpx, datetime as dt

app = FastAPI()
BOT = os.getenv("BOT_NAME","healthcare")

@app.get("/health")
def health(): return {"ok": True, "bot": BOT, "ts": dt.datetime.utcnow().isoformat()}

@app.get("/triage")
def triage(symptom: str):  # stub
    return {"bot": BOT, "symptom": symptom, "advice": "This is not medical advice. See a clinician."}
