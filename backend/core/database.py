import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Set up the SQLAlchemy engine
if DATABASE_URL:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None

def get_db_session():
    """Returns a new database session if configured."""
    if not SessionLocal:
        raise ValueError("DATABASE_URL is not set or invalid.")
    
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
