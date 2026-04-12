import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file to access sensitive configurations
load_dotenv()

# Retrieve the database connection URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")

# Initialize the SQLAlchemy components
# engine: The gateway to the database, handles connection pooling
# SessionLocal: A factory for creating new database session objects
if DATABASE_URL:
    # pool_pre_ping=True helps handle stale connections by checking connectivity before use
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
else:
    engine = None
    SessionLocal = None

def get_db_session():
    """
    Dependency generator for creating and closing database sessions.
    
    Yields:
        session: An active SQLAlchemy Session object.
        
    Raises:
        ValueError: If the database is not correctly configured.
    """
    if not SessionLocal:
        raise ValueError("DATABASE_URL is not set or invalid.")
    
    session = SessionLocal()
    try:
        yield session
    finally:
        # Ensure the session is closed even if an exception occurs during request processing
        session.close()
