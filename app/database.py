import os
from sqlmodel import create_engine, SQLModel

# Vercel automatically sets the "VERCEL" environment variable.
# We use this to check if the app is in production or running locally.
if os.environ.get("VERCEL"):
    # Write to the temporary folder allowed by Vercel
    sqlite_file_name = "/tmp/resume_database.db"
else:
    # Write to the local folder for your own development
    sqlite_file_name = "resume_database.db"

# Note the triple slashes for the URL format
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)