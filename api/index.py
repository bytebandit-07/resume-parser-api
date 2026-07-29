import os
import sys

# Add the root directory to path so imports like 'from app.database' work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from mangum import Mangum

# Import from your 'app' folder
from app.database import create_db_and_tables
from app.routers import resume

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Skip DB creation on Vercel (read-only filesystem)
    if not os.getenv("VERCEL"):
        create_db_and_tables()
    yield

app = FastAPI(
    title="AI Resume Parser API",
    description="Parse resumes using AI to extract structured information",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router)

@app.get("/")
async def root():
    return HTMLResponse(content="<h1>AI Resume Parser is Live! 🚀<br>Visit <a href='/docs'>/docs</a> for API documentation.</h1>")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Mangum handler for Vercel Serverless deployment
# Vercel's Python builder looks for 'handler'
handler = Mangum(app, lifespan="off")