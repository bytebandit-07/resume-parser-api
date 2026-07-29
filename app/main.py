import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.routers import resume
from mangum import Mangum

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Vercel par database creation skip karein (read-only filesystem crash se bachane ke liye)
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

# Static files mount (Local ke liye zaroori, Vercel isko ignore kar dega)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(resume.router)

@app.get("/")
async def root():
    # Vercel par static file serve karne ke liye safe fallback
    return HTMLResponse(content="<h1>AI Resume Parser is Live! 🚀<br>Visit <a href='/docs'>/docs</a> for API documentation.</h1>")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Mangum handler for Vercel Serverless deployment
handler = Mangum(app, lifespan="off")