from pathlib import Path
from fastapi import FastAPI, Form, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from database import create_db_and_tables
from auth import router as auth_router
from scheduler import start as start_scheduler
from gemini_utils import get_conversion_idea

app = FastAPI(title="Kıyafet Dönüştürücü API")
app.include_router(auth_router, tags=["auth"])

# ---------- Frontend ----------
BASE = Path(__file__).resolve().parent
FRONT_DIR = BASE / "frontend"
INDEX_FILE = FRONT_DIR / "index.html"
app.mount("/frontend", StaticFiles(directory=FRONT_DIR), name="frontend")


# ---------- Startup ----------
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    start_scheduler()


# ---------- Routes ----------
@app.get("/", response_class=HTMLResponse)
def root():
    if INDEX_FILE.exists():
        return INDEX_FILE.read_text(encoding="utf-8")
    raise HTTPException(404, "index.html not found")


@app.post("/suggest")
async def suggest(clothing_item: str = Form(...)):
    try:
        idea = await get_conversion_idea(clothing_item)
    except Exception as e:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, str(e))
    return {"idea": idea}
