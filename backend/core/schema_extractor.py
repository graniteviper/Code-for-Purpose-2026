from sqlalchemy import inspect
from core.database import engine

import json

def get_database_schema() -> dict:
    """
    Extracts the schema (tables, views, and columns) from the database
    and formats it as a JSON-compatible dictionary.
    """
    if not engine:
        return {"error": "No database connection available. Make sure DATABASE_URL is set."}
        
    inspector = inspect(engine)
    schema_details = {
        "tables": [],
        "views": []
    }
    
    # 1. Fetch standard tables
    tables = inspector.get_table_names()
    for table_name in tables:
        columns = inspector.get_columns(table_name)
        col_details = [{"name": col['name'], "type": str(col['type'])} for col in columns]
        schema_details["tables"].append({"name": table_name, "columns": col_details})
        
    # 2. Fetch views (since you specifically mentioned using views!)
    views = inspector.get_view_names()
    for view_name in views:
        columns = inspector.get_columns(view_name)
        col_details = [{"name": col['name'], "type": str(col['type'])} for col in columns]
        schema_details["views"].append({"name": view_name, "columns": col_details})
        
    return schema_details

if __name__ == "__main__":
    # If you run this file directly, it will print out your live database schema as JSON!
    print("Extracting schema from Neon DB...\n")
    schema_json = get_database_schema()
    print(json.dumps(schema_json, indent=2))
