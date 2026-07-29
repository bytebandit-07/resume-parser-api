from sqlmodel import SQLModel, create_engine, Session
import os

# Check if running on Vercel or Locally
if os.getenv("VERCEL"):
    DATABASE_URL = "sqlite:///:memory:"
else:
    DATABASE_URL = "sqlite:///./resumes.db"

engine = create_engine(DATABASE_URL, echo=False, connect_args={"check_same_thread": False})

def create_db_and_tables():
    try:
        SQLModel.metadata.create_all(engine)
    except Exception as e:
        print(f"Database creation error: {e}")
        pass  # Serverless environment me errors ignore karein

def get_session():
    with Session(engine) as session:
        yield session