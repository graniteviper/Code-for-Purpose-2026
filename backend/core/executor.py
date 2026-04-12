import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import json
from decimal import Decimal
from datetime import date, datetime

# Load env variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

FILE_PATH = "backend/data/sample_data.txt"

def serialize_value(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    return value


def serialize_row(row):
    return {key: serialize_value(value) for key, value in row.items()}

def get_all_tables(conn):
    result = conn.execute(
        text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
    )
    return [row[0] for row in result.fetchall()]

def get_sample_data():
    data = {}

    with engine.connect() as conn:
        tables = get_all_tables(conn)

        for table in tables:
            try:
                result = conn.execute(
                    text(f"SELECT * FROM {table} LIMIT 10")
                )
                rows = [
                    serialize_row(dict(row._mapping))
                    for row in result.fetchall()
                ]
                data[table] = rows

            except Exception as e:
                # Skip problematic tables
                data[table] = f"Error: {str(e)}"

    return data

def execute_sql_query(session: Session, sql: str):
    """
    Executes a SQL query against the database and returns the results.
    """
    try:
        result = session.execute(text(sql))
        # result.mappings() returns a sequence of mappings (dictionary-like objects)
        data = [dict(row) for row in result.mappings().fetchall()]
        return {"status": "success", "data": data}
    except Exception as e:
        return {"status": "error", "message": str(e)}
