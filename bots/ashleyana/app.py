import os, json, httpx
from datetime import datetime, time, timezone
from fastapi import FastAPI
from pydantic import BaseModel

BOT_NAME = os.getenv("BOT_NAME","bot")
TASKS_URL = os.getenv("TASKS_URL","")
AUTH_TOKEN = os.getenv("AUTH_TOKEN","devtoken")
SHIFT_START = os.getenv("SHIFT_START","00:00")
SHIFT_END   = os.getenv("SHIFT_END","06:00")

app = FastAPI(title=f"{BOT_NAME}-bot")

def in_shift(now_utc: datetime) -> bool:
    s_h,s_m = map(int, SHIFT_START.split(":"))
    e_h,e_m = map(int, SHIFT_END.split(":"))
    t = now_utc.time(); start, end = time(s_h,s_m), time(e_h,e_m)
    return (start <= t < end) if start < end else (t >= start or t < end)

async def fetch_tasks() -> list[dict]:
    if not TASKS_URL: return []
    async with httpx.AsyncClient(timeout=10) as cx:
        r = await cx.get(TASKS_URL); r.raise_for_status(); return r.json()

async def do_task(t: dict) -> str:
    k = t.get("type")
    if k=="advertise_free": return f"[{BOT_NAME}] advertise {t.get('limit',1000)} link={t.get('link','')}"
    if k=="bundle_models":  return f"[{BOT_NAME}] ensure RapidAlphaX/Healthcare bundled (spec task)"
    if k=="post_social":    return f"[{BOT_NAME}] post_social: {t.get('text','')[:120]}"
    if k=="build_apk":      return f"[{BOT_NAME}] build_apk requested (run locally via console)"
    return f"[{BOT_NAME}] unknown task: {k}"

class Push(BaseModel):
    token: str
    task: dict

@app.get("/health")
def health():
    now = datetime.now(timezone.utc)
    return {"bot": BOT_NAME, "utc": now.isoformat(), "in_shift": in_shift(now)}

@app.post("/task")
async def push(p: Push):
    if p.token != AUTH_TOKEN: return {"ok": False, "error": "unauthorized"}
    msg = await do_task(p.task); return {"ok": True, "msg": msg}

@app.get("/")
async def run_cycle():
    now = datetime.now(timezone.utc)
    if not in_shift(now): return {"bot": BOT_NAME, "status":"off-shift"}
    out=[]; 
    for t in await fetch_tasks():
        if BOT_NAME in t.get("targets",[BOT_NAME]): out.append(await do_task(t))
    return {"bot": BOT_NAME, "ran": out or ["no tasks"]}
