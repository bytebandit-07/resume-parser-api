import os
from sqlmodel import create_engine, SQLModel

# Agar Vercel par hai toh /tmp use karo, warna local folder
if os.environ.get("VERCEL"):
    sqlite_file_name = "/tmp/resume_database.db"
else:
    sqlite_file_name = "resume_database.db"

sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)