from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models.schemas import ParsedResume
from app.services.ai_service import parse_resume_with_ai
from datetime import datetime
import io
import os
from PyPDF2 import PdfReader
from docx import Document

router = APIRouter(prefix="/resume", tags=["resume"])

# Check if running on Vercel (skip DB operations)
IS_VERCEL = os.getenv("VERCEL") is not None

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF file"""
    try:
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
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


@router.post("/parse-file")
async def parse_resume_file(file: UploadFile = File(...)):
    """Parse resume from uploaded PDF or DOCX file"""
    try:
        # Read file content
        contents = await file.read()
        
        # Extract text based on file type
        if file.filename.lower().endswith('.pdf'):
            resume_text = extract_text_from_pdf(contents)
        elif file.filename.lower().endswith('.docx'):
            resume_text = extract_text_from_docx(contents)
        else:
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported")
        
        if not resume_text or len(resume_text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Could not extract text from file")
        
        # Parse with AI
        parsed_data = parse_resume_with_ai(resume_text)
        
        # Save to database only if NOT on Vercel
        resume_id = 0
        if not IS_VERCEL:
            try:
                from app.database import get_session
                from app.models.schemas import ResumeDB
                from sqlmodel import Session
                
                gen = get_session()
                session = next(gen)
                db_resume = ResumeDB(
                    original_text=resume_text,
                    parsed_data=parsed_data.model_dump_json()
                )
                session.add(db_resume)
                session.commit()
                session.refresh(db_resume)
                resume_id = db_resume.id
            except Exception as db_err:
                print(f"DB save skipped: {db_err}")
        
        return {
            "id": resume_id,
            "parsed_data": parsed_data.model_dump(),
            "created_at": datetime.utcnow().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in parse_resume_file: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")


@router.post("/parse-text")
async def parse_resume_text(text: str = Form(...)):
    """Parse resume from plain text"""
    try:
        if not text or len(text.strip()) < 10:
            raise HTTPException(status_code=400, detail="Text too short")
        
        parsed_data = parse_resume_with_ai(text)
        
        resume_id = 0
        if not IS_VERCEL:
            try:
                from app.database import get_session
                from app.models.schemas import ResumeDB
                
                gen = get_session()
                session = next(gen)
                db_resume = ResumeDB(
                    original_text=text,
                    parsed_data=parsed_data.model_dump_json()
                )
                session.add(db_resume)
                session.commit()
                session.refresh(db_resume)
                resume_id = db_resume.id
            except Exception as db_err:
                print(f"DB save skipped: {db_err}")
        
        return {
            "id": resume_id,
            "parsed_data": parsed_data.model_dump(),
            "created_at": datetime.utcnow().isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in parse_resume_text: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")