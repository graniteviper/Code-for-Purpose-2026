from fastapi import APIRouter
from models.request_models import QueryRequest

# TEMP: no real imports yet
# from core.planner import QueryPlanner
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from core.database import get_db_session

router = APIRouter()

# @router.post("/query")
# def handle_query(request: QueryRequest, db: Session = Depends(get_db_session)):
#     query = request.query

#     print("Incoming query:", query)

#     # 🧠 Step 1: planner (placeholder)
#     plan = fake_planner(query)

#     # ⚙️ Step 2: SQL generator (placeholder)
#     sql = fake_sql_generator(plan)

#     # 🗄️ Step 3: execution (placeholder)
#     data = fake_executor(sql, db)

#     # 🧠 Step 4: explanation (placeholder)
#     explanation = fake_explainer(query, data)

#     return {
#         "query": query,
#         "plan": plan,
#         "sql": sql,
#         "data": data,
#         "explanation": explanation
#     }

from core.planner import plan_query

@router.post("/query")
def handle_query(request: QueryRequest):
    query = request.query
    
    # 🧠 Step 1: Execute planner logic using regex categorized words
    plan = plan_query(query)
    
    return {
        "query": query,
        "plan": plan,
        "message": "Query categorized successfully"
    }

# Remove the unused fake functions for now so the code is cleaner