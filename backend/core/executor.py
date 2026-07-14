import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import json
from decimal import Decimal
from datetime import date, datetime

# Load environment variables to ensure database connectivity
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
else:
    engine = None

# Path to cache or read sample data from
FILE_PATH = "backend/data/sample_data.txt"

def serialize_value(value):
    """
    Utility function to convert non-JSON-serializable types into serializable formats.
    
    Args:
        value: The value to serialize (could be Decimal, date, datetime).
        
    Returns:
        The serialized version of the value (float for Decimal, ISO string for dates).
    """
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def serialize_row(row):
    """
    Serializes an entire database row by applying serialize_value to each column.
    
    Args:
        row: A dictionary representing a database row.
        
    Returns:
        A dictionary with all values converted to serializable types.
    """
    return {key: serialize_value(value) for key, value in row.items()}

def get_all_tables(conn):
    """
    Fetches the names of all public tables in the database.
    
    Args:
        conn: An active database connection.
        
    Returns:
        A list of table name strings.
    """
    result = conn.execute(
        text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    )
    return [row[0] for row in result.fetchall()]

def get_sample_data():
    """
    Retrieves a small sample of data (up to 10 rows) from every table in the public schema.
    This is used to provide context to the LLM about the actual data values.
    
    Returns:
        A dictionary where keys are table names and values are lists of sampled rows.
    """
    if not engine:
        return {}
        
    data = {}

    with engine.connect() as conn:
        tables = get_all_tables(conn)

        for table in tables:
            try:
                # Limit the sample size to keep the context window manageable
                result = conn.execute(
                    text(f"SELECT * FROM {table} LIMIT 10")
                )
                rows = [
                    serialize_row(dict(row._mapping))
                    for row in result.fetchall()
                ]
                data[table] = rows

            except Exception as e:
                # If a table cannot be read (e.g., permissions), record the error for debugging
                data[table] = f"Error: {str(e)}"

    return data

def execute_sql_query(session: Session, sql: str):
    """
    Executes a raw SQL query against the database and returns a structured response.
    
    Args:
        session: An active SQLAlchemy Session.
        sql: The raw SQL string to execute.
        
    Returns:
        A dictionary containing the execution status ('success' or 'error') and the resulting data.
    """
    try:
        result = session.execute(text(sql))
        # result.mappings() returns a sequence of mappings (dictionary-like objects)
        data = [dict(row) for row in result.mappings().fetchall()]
        return {"status": "success", "data": data}
    except Exception as e:
        # Catch and return any database errors during execution
        return {"status": "error", "message": str(e)}
