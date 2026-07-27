import os
from sqlmodel import create_engine, SQLModel

# Agar Vercel par hai toh In-Memory DB use karo (no files created)
if os.environ.get("VERCEL") or os.environ.get("VERCEL_ENV"):
    sqlite_url = "sqlite:///:memory:"
else:
    # Local development ke liye file banayega
    sqlite_file_name = "resume_database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)