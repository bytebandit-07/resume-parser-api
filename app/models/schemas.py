from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

# Database Model
class ResumeDB(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    original_text: str
    parsed_data: str  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Request/Response Schemas
class ResumeRequest(BaseModel):
    text: str

class ParsedResume(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    skills: list[str] = []
    experience_years: Optional[int] = None
    education: list[str] = []
    summary: Optional[str] = None

class ResumeResponse(BaseModel):
    id: int
    parsed_data: ParsedResume
    created_at: datetime