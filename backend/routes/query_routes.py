from fastapi import APIRouter, Depends
from models.request_models import QueryRequest
from core.get_sql_from_llm import SQLGenerator, validate_sql
from core.explainer_data import ExplanationGenerator
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db_session
from core.planner import plan_query
from core.schema_extractor import get_database_schema
from core.executor import execute_sql_query
from core.table_finder import detect_query_scope

# Initialize the router for data-related endpoints
router = APIRouter()


@router.post("/query")
def handle_query(request: QueryRequest, db: Session = Depends(get_db_session)):
    """
    Main endpoint for processing natural language queries.
    This routes the request through a four-step pipeline:
    1. Intent Classification (Planner)
    2. SQL Generation (LLM)
    3. Query Execution (DB)
    4. Result Explanation (LLM)
    """
    query = request.query
    print("Incoming query:", query)

    # 🧠 Step 1: Classify the query intent (Comparison, Breakdown, etc.)
    # This helps guide the SQL generator and the final explainer.
    parsed_json = plan_query(query)

    # Get the current dynamic database schema for context
    db_schema_json = get_database_schema()
    table_required = detect_query_scope(query)
    # ⚙️ Step 2: Generate the PostgreSQL query using the LLM
    sql_gen = SQLGenerator()
    sql = sql_gen.generate_sql(query, parsed_json, db_schema_json, table_required)

    # Perform safety validation on the generated SQL to block destructive commands
    if not validate_sql(sql):
        return {"error": "Unsafe SQL generated"}

    # 🗄️ Step 3: Execute the validated SQL against the database
    execution_result = execute_sql_query(db, sql)
    
    # Handle any execution errors (e.g., syntax issues or missing tables)
    if execution_result["status"] == "error":
        return {"error": f"Failed to execute SQL: {execution_result['message']}", "sql": sql}
        
    data = execution_result["data"]

    # 🧠 Step 4: Generate a human-readable explanation of the data results
    # This translates raw JSON data into business insights.
    explanation = ExplanationGenerator().generate(query, data, parsed_json["category"])

    # Return the full processing result to the frontend
    return {
        "query": query,
        "plan": parsed_json,
        "sql": sql,
        "data": data,
        "explanation": explanation
    }
