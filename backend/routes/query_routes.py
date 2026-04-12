from fastapi import APIRouter
from models.request_models import QueryRequest
from core.get_sql_from_llm import SQLGenerator, validate_sql

# TEMP: no real imports yet
# from core.planner import QueryPlanner
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db_session

from core.planner import plan_query
from core.schema_extractor import get_database_schema
from core.executor import execute_sql_query

router = APIRouter()


@router.post("/query")
def handle_query(request: QueryRequest, db: Session = Depends(get_db_session)):
    query = request.query

    print("Incoming query:", query)

    # 🧠 Step 1: planner (placeholder)
    parsed_json = plan_query(query)

    # Get dynamic DB schema
    db_schema_json = get_database_schema()
    print(db_schema_json)
    # ⚙️ Step 2: SQL generator
    sql_gen = SQLGenerator()

    sql = sql_gen.generate_sql(query, parsed_json, db_schema_json)

    if not validate_sql(sql):
        return {"error": "Unsafe SQL generated"}

    # print("Generated SQL:", sql)
    # 🗄️ Step 3: execution
    execution_result = execute_sql_query(db, sql)
    
    if execution_result["status"] == "error":
        return {"error": f"Failed to execute SQL: {execution_result['message']}", "sql": sql}
        
    data = execution_result["data"]

    # 🧠 Step 4: explanation (placeholder)
    # explanation = fake_explainer(query, data)

    return {
        "query": query,
        "plan": parsed_json,
        "sql": sql,
        "data": data,
        "explanation": "explanation"
    }
