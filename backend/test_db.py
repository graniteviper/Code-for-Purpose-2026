from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from core.schema_extractor import get_database_schema
from core.executor import execute_sql_query, get_sample_data    
from core.get_sql_from_llm import SQLGenerator, validate_sql

"""
Manual Database Integration Test script.
Verifies the full pipeline (Schema Extraction -> SQL Generation -> Execution)
against the live Neon database using environment variables.
Run with: python backend/test_db.py
"""

# Load environment variables from .env file
load_dotenv()

# --- Database Engine Setup ---
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("WARNING: DATABASE_URL not found in environment variables.")

# Create a local engine and session factory for testing
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def test():
    """
    Simulates a single query lifecycle for manual verification.
    """
    session = SessionLocal()

    # Define a test user query
    user_query = "average price of product name Headphones"

    # Mock classification results
    parsed_json = {
        "category": "comparison"
    }
    
    # 1. Fetch dynamic context (Sample data and Schema)
    sample_data = get_sample_data()
    db_schema_json = get_database_schema()
    
    # 2. Generate the SQL query via the LLM
    sql_gen = SQLGenerator()
    sql = sql_gen.generate_sql(user_query, parsed_json, db_schema_json, session)

    # 3. Perform a safety check on the generated SQL
    if not validate_sql(sql):
        print("❌ Unsafe SQL generated")
        session.close()
        return

    # 4. Execute the SQL and print the results
    result = execute_sql_query(session, sql)

    print("\n[INFO] Generated SQL:\n", sql)
    print("\n[INFO] Query Result:\n", result)

    session.close()

if __name__ == "__main__":
    print("Running manual DB integration test...")
    test()
