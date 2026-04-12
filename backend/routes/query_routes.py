from fastapi import APIRouter
from models.request_models import QueryRequest
from core.get_sql_from_llm import SQLGenerator, validate_sql

# TEMP: no real imports yet
# from core.planner import QueryPlanner

router = APIRouter()

@router.post("/query")
def handle_query(request: QueryRequest):
    query = request.query

    print("Incoming query:", query)

    # 🧠 Step 1: planner (placeholder)
    # parsed_json = fake_planner(query)
    parsed_json = {
  "category": "breakdown",
  "metric": "revenue",
  "time_range": "last month",
  "filters": {"category": "grocery"},
  "group_by": "product_name"
}

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




def fake_planner(query):
    return {
        "category": "breakdown",
        "note": "planner not implemented yet"
    }

def fake_sql_generator(plan):
    return "SELECT * FROM inventory LIMIT 5;"

def fake_executor(sql):
    return [
        {"product": "Apple", "revenue": 100},
        {"product": "Milk", "revenue": 200}
    ]

def fake_explainer(query, data):
    return "This is a placeholder explanation."