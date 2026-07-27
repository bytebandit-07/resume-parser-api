from sqlmodel import SQLModel, create_engine, Session

# In-memory database for Vercel serverless deployment
DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(DATABASE_URL, echo=False)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session