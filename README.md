#  AI Resume Parser API

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/AI-Groq_Llama3-f55036.svg)](https://groq.com/)
[![Deployment](https://img.shields.io/badge/Deployed_on-Vercel-000000.svg)](https://vercel.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An intelligent, full-stack web application that automates resume screening by extracting structured data (skills, experience, education, contact info) from PDF and DOCX documents using state-of-the-art Large Language Models (LLMs).

 **Live Demo:** [https://resume-parser-api-44bg.vercel.app/](https://resume-parser-api-44bg.vercel.app/)  
 **API Documentation:** [https://resume-parser-api-44bg.vercel.app/docs](https://resume-parser-api-44bg.vercel.app/docs)

---

##  Features

-  **Multi-Format Support:** Seamlessly parses `.pdf` and `.docx` resume files.
-  **AI-Powered Extraction:** Utilizes Groq's ultra-fast Llama 3 models for accurate, context-aware data extraction.
-  **Structured Output:** Returns clean, validated JSON containing Name, Email, Phone, Skills, Experience, Education, and Professional Summary.
-  **Modern UI:** Responsive, drag-and-drop frontend built with vanilla HTML/CSS/JS (no heavy frameworks required).
-  **Serverless Optimized:** Deployed on Vercel with optimized timeout handling and in-memory database fallback for instant scalability.
-  **Robust Error Handling:** Graceful fallbacks (regex-based extraction) if the AI service temporarily fails.

---

##  Tech Stack

| Category | Technology |
| :--- | :--- |
| **Backend Framework** | FastAPI (Python 3.10+) |
| **AI / LLM** | Groq API (`llama-3.1-8b-instant` / `llama-3.3-70b-versatile`) |
| **Database / ORM** | SQLModel (SQLite for local, In-Memory for serverless) |
| **Document Parsing** | `PyPDF2`, `python-docx` |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript (Fetch API) |
| **Deployment** | Vercel (Serverless Functions) |
| **Version Control** | Git & GitHub |

---

##  Architecture & Workflow

1. **Upload:** User uploads a resume (PDF/DOCX) or pastes text via the web interface.
2. **Extraction:** Backend extracts raw text using `PyPDF2` or `python-docx`.
3. **AI Processing:** Raw text is sent to Groq API with a strict JSON-schema prompt.
4. **Validation:** Response is validated against Pydantic/SQLModel schemas.
5. **Display:** Structured data is returned to the frontend and displayed as interactive tags and cards.

---

##  Local Development Setup

Follow these steps to run the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/bytebandit-07/resume-parser-api.git
cd resume-parser-api
