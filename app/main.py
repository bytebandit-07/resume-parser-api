from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.database import create_db_and_tables
from app.routers import resume

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

# Include routers
app.include_router(resume.router)

@app.get("/")
async def root():
    return {
        "message": "AI Resume Parser API",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}