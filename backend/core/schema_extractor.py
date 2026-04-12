from sqlalchemy import inspect
from core.database import engine

import json

def get_database_schema() -> dict:
    """
    Extracts the current database schema (tables, views, and their columns).
    This structural information is crucial for the LLM to generate syntactically correct SQL.
    
    Returns:
        dict: A dictionary containing 'tables' and 'views', each with names and column details.
              Returns an error dictionary if the database is not connected.
    """
    # Check if the database engine is initialized
    if not engine:
        return {"error": "No database connection available. Make sure DATABASE_URL is set."}
        
    # Create an inspector object to probe the database structure
    inspector = inspect(engine)
    schema_details = {
        "tables": [],
        "views": []
    }
    
    # 1. Fetch standard physical tables
    tables = inspector.get_table_names()
    for table_name in tables:
        # Get column names and types for each table
        columns = inspector.get_columns(table_name)
        col_details = [{"name": col['name'], "type": str(col['type'])} for col in columns]
        schema_details["tables"].append({"name": table_name, "columns": col_details})
        
    # 2. Fetch database views
    # Views are handled separately in PostgreSQL for clarity
    views = inspector.get_view_names()
    for view_name in views:
        # Get column names and types for each view
        columns = inspector.get_columns(view_name)
        col_details = [{"name": col['name'], "type": str(col['type'])} for col in columns]
        schema_details["views"].append({"name": view_name, "columns": col_details})
        
    return schema_details

if __name__ == "__main__":
    # This block allows for manual verification of the schema extractor.
    # When run directly, it will extract and print the live schema as a JSON object.
    print("Extracting schema from Neon DB...\n")
    schema_json = get_database_schema()
    
    # Pretty-print the schema for easier reading
    print(json.dumps(schema_json, indent=2))
