import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class SQLGenerator:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_sql(self, user_query, parsed_json):
        prompt = build_sql_prompt(user_query, parsed_json)

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

def build_sql_prompt(user_query, parsed_json):
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

Table: inventory
Columns:
- date (DATE)
- product_name (TEXT)
- category (TEXT)
- quantity_sold (INT)
- revenue (NUMERIC)

----------------------------------------
CATEGORY DEFINITIONS:

1. change_analysis:
- Compare two time periods
- Identify increase/decrease
- Group by category or product
- Focus on drivers of change

2. breakdown:
- Group data by category/product
- Show contribution using SUM(metric)

3. comparison:
- Compare entities (products/categories)
- Filter specific values if provided
- Use aggregation and sorting

4. summary:
- Provide total or average
- Optionally group by time (daily/weekly)

----------------------------------------
RULES:

- ONLY generate SQL (no explanation)
- ONLY use SELECT queries
- NEVER use DELETE, UPDATE, INSERT, DROP
- Use correct GROUP BY when aggregating
- Use WHERE for filters (category, product, time)
- Use ORDER BY for ranking
- Use LIMIT when appropriate (e.g., top results)

----------------------------------------
OUTPUT:
Return ONLY valid PostgreSQL SQL query.
"""