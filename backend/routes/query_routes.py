from fastapi import APIRouter
from models.request_models import QueryRequest
from core.get_sql_from_llm import SQLGenerator, validate_sql

# TEMP: no real imports yet
# from core.planner import QueryPlanner
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db_session

router = APIRouter()

from core.planner import plan_query

@router.post("/query")
def handle_query(request: QueryRequest):
    query = request.query

    print("Incoming query:", query)

    # 🧠 Step 1: planner (placeholder)
    parsed_json = plan_query(query)

    # ⚙️ Step 2: SQL generator (placeholder)
    sql_gen = SQLGenerator()

    sql = sql_gen.generate_sql(query, parsed_json)

    if not validate_sql(sql):
        return {"error": "Unsafe SQL generated"}

    # print("Generated SQL:", sql)
    # 🗄️ Step 3: execution (placeholder)
    # data = fake_executor(sql)

    # 🧠 Step 4: explanation (placeholder)
    # explanation = fake_explainer(query, data)

    return {
        "query": query,
        "plan": parsed_json,
        "sql": sql,
        "data": "data",
        "explanation": "explanation"
    }
