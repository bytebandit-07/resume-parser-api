from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import ResumeDB, ResumeRequest, ResumeResponse, ParsedResume
from app.services.ai_service import parse_resume_with_ai
import json

router = APIRouter(prefix="/resume", tags=["resume"])

@router.post("/parse", response_model=ResumeResponse)
async def parse_resume(
    resume_data: ResumeRequest,
    session: Session = Depends(get_session)
):
    """Parse resume text using AI"""
    
    # Parse with AI
    parsed_data = parse_resume_with_ai(resume_data.text)
    
    # Save to database
    db_resume = ResumeDB(
        original_text=resume_data.text,
        parsed_data=parsed_data.model_dump_json()
    )
    session.add(db_resume)
    session.commit()
    session.refresh(db_resume)
    
    return ResumeResponse(
        id=db_resume.id,
        parsed_data=parsed_data,
        created_at=db_resume.created_at
    )

@router.get("/{resume_id}", response_model=ResumeResponse)
async def get_parsed_resume(
    resume_id: int,
    session: Session = Depends(get_session)
):
    """Get a previously parsed resume"""
    
    db_resume = session.get(ResumeDB, resume_id)
    if not db_resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    parsed_data = ParsedResume(**json.loads(db_resume.parsed_data))
    
    return ResumeResponse(
        id=db_resume.id,
        parsed_data=parsed_data,
        created_at=db_resume.created_at
    )

@router.get("/")
async def list_all_resumes(session: Session = Depends(get_session)):
    """List all parsed resumes"""
    
    resumes = session.query(ResumeDB).all()
    return {
        "total": len(resumes),
        "resumes": [
            {
                "id": r.id,
                "created_at": r.created_at,
                "preview": r.original_text[:100] + "..."
            }
            for r in resumes
        ]
    }