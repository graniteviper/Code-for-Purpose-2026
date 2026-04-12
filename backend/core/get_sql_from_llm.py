from core.executor import get_sample_data
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Initialize environment variables
load_dotenv()

class SQLGenerator:
    """
    Handles the generation of SQL queries using the Gemini LLM.
    """
    def __init__(self):
        # Configure the Generative AI client
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generate_sql(self, user_query, parsed_json, db_schema, table_required):
        """
        Takes a natural language query and intent, and returns a valid SQL string.
        
        Args:
            user_query: The raw string from the user.
            parsed_json: The classification and metadata from the planner.
            db_schema: The current structure of the database.
            
        Returns:
            A string containing the generated SQL query.
        """
        # Fetch actual data samples to help the LLM understand valid filter values
        sample_rows = get_sample_data()
        
        # Construct the detailed prompt for the LLM
        prompt = build_sql_prompt(user_query, parsed_json, db_schema, sample_rows, table_required)

        # Get the response from the model
        response = self.model.generate_content(prompt)

        sql = response.text.strip()

        # 🔐 Safety cleanup: remove markdown markers and whitespace
        sql = sql.replace("```sql", "").replace("```", "").strip()

        return sql


def validate_sql(sql):
    """
    Performs basic safety checks on the generated SQL to prevent destructive operations.
    
    Args:
        sql: The SQL string to validate.
        
    Returns:
        bool: True if the SQL is considered safe (SELECT only), False otherwise.
    """
    sql_lower = sql.lower()

    # We only permit SELECT queries for data retrieval
    if not sql_lower.startswith("select"):
        return False

    # Block keywords that could modify or delete data
    blocked = ["drop", "delete", "update", "insert"]
    if any(word in sql_lower for word in blocked):
        return False

    return True

def build_sql_prompt(user_query, parsed_json, db_schema, sample_rows, table_required):
    """
    Constructs the master prompt for the SQL generation task.
    Includes schema documentation, rules, and few-shot-like guidance from sample data.
    
    Args:
        user_query: The user's question.
        parsed_json: The intent from the planner.
        db_schema: The database structure.
        sample_rows: Actual values for context.
        
    Returns:
        str: The complete prompt for the LLM.
    """
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

Tables of FOCUS:
{table_required}

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
