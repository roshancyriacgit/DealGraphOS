
import os
import webbrowser
import threading
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn

from .api import deals, intelligence

from .models.db import init_db

app = FastAPI(title="DealGraphOS", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(deals.router, prefix="/api/deals", tags=["deals"])
app.include_router(intelligence.router, prefix="/api/intelligence", tags=["intelligence"])


@app.on_event("startup")
async def startup_event():
    init_db()


# Static frontend
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend_build"

if FRONTEND_DIR.exists():
    app.mount("/app", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="app")


@app.get("/", include_in_schema=False)
async def index():
    if FRONTEND_DIR.exists():
        return FileResponse(FRONTEND_DIR / "index.html")
    return {"message": "DealGraphOS backend is running. Frontend not found."}


def open_browser(port: int):
    url = f"http://127.0.0.1:{port}"
    try:
        webbrowser.open(url)
    except Exception:
        pass


def run():
    port = int(os.environ.get("DEALGRAPHOS_PORT", "8137"))
    threading.Timer(1.0, open_browser, args=(port,)).start()
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)


if __name__ == "__main__":
    run()
