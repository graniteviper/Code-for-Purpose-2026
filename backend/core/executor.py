from sqlalchemy import text
from sqlalchemy.orm import Session

def get_sample_data(db):
    result = db.execute(text("SELECT * FROM kaggle_products LIMIT 20"))
    rows = [dict(row._mapping) for row in result.fetchall()]
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
