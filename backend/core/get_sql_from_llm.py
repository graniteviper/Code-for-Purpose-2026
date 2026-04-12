from core.executor import get_sample_data
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class SQLGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_sql(self, user_query, parsed_json, db_schema):
        sample_rows = get_sample_data()
        # print(sample_rows)
        prompt = build_sql_prompt(user_query, parsed_json, db_schema, sample_rows)

        response = self.model.generate_content(prompt)

        sql = response.text.strip()

        # 🔐 Safety cleanup (important)
        sql = sql.replace("```sql", "").replace("```", "").strip()

        return sql


def validate_sql(sql):
    sql_lower = sql.lower()

    if not sql_lower.startswith("select"):
        return False

    blocked = ["drop", "delete", "update", "insert"]
    if any(word in sql_lower for word in blocked):
        return False

    return True

def build_sql_prompt(user_query, parsed_json, db_schema, sample_rows):
    return f"""
You are an expert PostgreSQL data analyst.

Your task is to generate a SQL query based on a structured user request.

----------------------------------------
USER QUERY:
{user_query}

PARSED INTENT:
{parsed_json}

----------------------------------------
DATABASE SCHEMA:
{db_schema}

----------------------------------------
SAMPLE DATA (IMPORTANT - USE THIS TO UNDERSTAND VALUES):
{sample_rows}

----------------------------------------
INSTRUCTIONS:

- Use SAMPLE DATA to understand:
  • valid product_name values (e.g., Laptop, Monitor)
  • valid product_category values (e.g., Electronics, Clothing)
  • realistic filters (e.g., product_name = 'Laptop')

- If user mentions:
  • product → use product_name
  • category → use product_category
  • id → use product_id

- Prefer filtering using exact values seen in SAMPLE DATA

----------------------------------------
CATEGORY DEFINITIONS:

1. change_analysis:
- Compare across time (manufacture_date if needed)
- Identify increase/decrease
- Group by product or category

2. breakdown:
- GROUP BY product_name or product_category
- Use SUM() for aggregation

3. comparison:
- Compare entities (Laptop vs Monitor, etc.)
- Use WHERE with IN (...)
- Use aggregation if needed

4. summary:
- Use SUM / AVG
- No unnecessary grouping

----------------------------------------
STRICT RULES:

- ONLY generate SQL (no explanation)
- ONLY SELECT queries
- NEVER use DELETE, UPDATE, INSERT, DROP
- Use correct GROUP BY when aggregating
- Use WHERE for filtering
- Use ORDER BY for ranking
- Use LIMIT when useful
- Prefer explicit column names (NO SELECT *)

----------------------------------------
OUTPUT:
Return ONLY valid PostgreSQL SQL query.
"""