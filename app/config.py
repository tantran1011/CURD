import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Load environment variables from .env file
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = DATABASE_URL.encode('utf-8').decode('unicode_escape') if DATABASE_URL else None
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

# Create a new SQLAlchemy engine instance
engine = create_engine(DATABASE_URL, echo=True)
# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
