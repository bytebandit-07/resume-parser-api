import os
import json
import re
from groq import Groq
from dotenv import load_dotenv
from app.models.schemas import ParsedResume

load_dotenv()

def get_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set!")
    return Groq(api_key=api_key)


def parse_resume_with_ai(resume_text: str) -> ParsedResume:
    """Use Groq AI to parse resume text into structured data"""
    
    client = get_groq_client()
    
    # Limit resume text (rakho reasonable size)
    if len(resume_text) > 6000:
        resume_text = resume_text[:6000]
    
    # Shorter, more direct prompt
    prompt = f"""Extract resume information as JSON.

Resume:
{resume_text}

Return ONLY this JSON structure:
{{"name":"...","email":"...","phone":"...","skills":["..."],"experience_years":0,"education":["..."],"summary":"..."}}"""
    
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You extract resume data as JSON. Return only valid JSON, no markdown, no explanations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=2000,  # ✅ INCREASED from 800 to 2000
            response_format={"type": "json_object"}
        )
        
        content = completion.choices[0].message.content.strip()
        
        # Clean markdown if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        result = json.loads(content)
        return ParsedResume(**result)
    
    except Exception as e:
        print(f"AI parsing error: {e}")
        import traceback
        traceback.print_exc()
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