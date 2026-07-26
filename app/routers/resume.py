from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session
from app.database import get_session
from app.models.schemas import ResumeDB, ResumeResponse, ParsedResume
from app.services.ai_service import parse_resume_with_ai
import json
import io
from PyPDF2 import PdfReader
from docx import Document

router = APIRouter(prefix="/resume", tags=["resume"])

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"PDF parsing error: {str(e)}")

def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from Word file"""
    try:
        doc = Document(io.BytesIO(file_bytes))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"DOCX parsing error: {str(e)}")

@router.post("/parse-file", response_model=ResumeResponse)
async def parse_resume_file(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    """Parse resume from uploaded PDF or DOCX file"""
    
    # Read file content
    contents = await file.read()
    
    # Extract text based on file type
    if file.filename.endswith('.pdf'):
        resume_text = extract_text_from_pdf(contents)
    elif file.filename.endswith('.docx'):
        resume_text = extract_text_from_docx(contents)
    else:
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
    
    if not resume_text or len(resume_text.strip()) < 10:
        raise HTTPException(status_code=400, detail="Could not extract text from file")
    
    # Parse with AI
    parsed_data = parse_resume_with_ai(resume_text)
    
    # Save to database
    db_resume = ResumeDB(
        original_text=resume_text,
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

@router.post("/parse-text", response_model=ResumeResponse)
async def parse_resume_text(
    text: str,
    session: Session = Depends(get_session)
):
    """Parse resume from plain text"""
    
    parsed_data = parse_resume_with_ai(text)
    
    db_resume = ResumeDB(
        original_text=text,
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