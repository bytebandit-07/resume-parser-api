import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from app.models.schemas import ParsedResume

load_dotenv()

# Client ko function ke andar banayenge taake import time par crash na ho
def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set!")
    return Groq(api_key=api_key)

def parse_resume_with_ai(resume_text: str) -> ParsedResume:
    """Use Groq AI to parse resume text into structured data"""
    
    # Yahan client initialize karein
    client = get_groq_client()
    
    prompt = f"""
    You are a resume parser. Extract the following information from this resume text:
    - name (full name)
    - email
    - phone
    - skills (list of technical and soft skills)
    - experience_years (total years of experience as integer)
    - education (list of degrees/institutions)
    - summary (brief professional summary)
    
    Resume text:
    {resume_text}
    
    Return ONLY valid JSON in this exact format:
    {{
        "name": "string or null",
        "email": "string or null",
        "phone": "string or null",
        "skills": ["skill1", "skill2"],
        "experience_years": number or null,
        "education": ["education1", "education2"],
        "summary": "string or null"
    }}
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts structured data from resumes. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(completion.choices[0].message.content)
        return ParsedResume(**result)
    
    except Exception as e:
        print(f"AI parsing error: {e}")
        return extract_basic_info(resume_text)

def extract_basic_info(text: str) -> ParsedResume:
    """Fallback: Basic regex-based extraction"""
    
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\+?\d{10,15}'
    
    email = re.search(email_pattern, text)
    phone = re.search(phone_pattern, text)
    
    return ParsedResume(
        email=email.group(0) if email else None,
        phone=phone.group(0) if phone else None,
        skills=["Parsing failed - check API key"],
        summary="AI parsing unavailable"
    )