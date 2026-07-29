import os
import sys
from pathlib import Path

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from contextlib import asynccontextmanager
from mangum import Mangum

from app.database import create_db_and_tables
from app.routers import resume

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.getenv("VERCEL"):
        create_db_and_tables()
    yield

app = FastAPI(
    title="AI Resume Parser API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(resume.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = BASE_DIR / "static" / "index.html"
    if index_path.exists():
        return FileResponse(index_path)
    return HTMLResponse("<h1>index.html not found</h1>")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

handler = Mangum(app, lifespan="off")

@app.get("/favicon.ico")
async def favicon():
    return FileResponse(BASE_DIR / "static" / "favicon.ico") if (BASE_DIR / "static" / "favicon.ico").exists() else HTMLResponse(status_code=204)