import os
import sys
from pathlib import Path

# Add project root to Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from app.database import create_db_and_tables
from app.routers import resume

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

# Mount static files
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include your routers
app.include_router(resume.router)

@app.get("/", response_class=HTMLResponse)
async def root():
    index_path = BASE_DIR / "static" / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return HTMLResponse("<h1>Welcome - index.html not found</h1>")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# NO Mangum needed - Vercel's @vercel/python handles ASGI natively now