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


def get_sample_data():
    # 1. Try file
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            content = f.read().strip()
            if content:
                try:
                    return json.loads(content)
                except:
                    pass

    # 2. Fetch from DB
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM kaggle_products LIMIT 20"))
        rows = [serialize_row(dict(row._mapping)) for row in result.fetchall()]

    # 3. Save
    os.makedirs(os.path.dirname(FILE_PATH), exist_ok=True)
    with open(FILE_PATH, "w") as f:
        json.dump(rows, f)

    return rows

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
