from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.routers import resume
from mangum import Mangum  # <-- Vercel ke liye import kiya

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    create_db_and_tables()
    yield
    # Shutdown: Cleanup if needed

app = FastAPI(
    title="AI Resume Parser API",
    description="Parse resumes using AI to extract structured information",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware (for frontend integration if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files mount
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(resume.router)

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Mangum handler for Vercel Serverless deployment
handler = Mangum(app, lifespan="off")