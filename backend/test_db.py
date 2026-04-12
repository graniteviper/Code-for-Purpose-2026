from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from core.schema_extractor import get_database_schema
from core.executor import execute_sql_query, get_sample_data    
from core.get_sql_from_llm import SQLGenerator, validate_sql

load_dotenv()

# 🔹 DB setup
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# 🔹 schema (keep simple)
DB_SCHEMA = """
inventory(
  date,
  product_name,
  category,
  quantity_sold,
  revenue
)
"""

def test():
    session = SessionLocal()

    # 🔹 input query
    user_query = "average price of product name Headphones"

    # 🔹 minimal parsed json (since you're skipping full parser)
    parsed_json = {
        "category": "comparison"
    }
    sample_data = get_sample_data()
    db_schema_json = get_database_schema()
    # print(db_schema_json)
    # 🔹 generate SQL
    sql_gen = SQLGenerator()
    sql = sql_gen.generate_sql(user_query, parsed_json, db_schema_json, session)

    # print("\nGenerated SQL:\n", sql)

    # 🔐 validate
    if not validate_sql(sql):
        print("❌ Unsafe SQL generated")
        return

    # 🗄️ execute
    result = execute_sql_query(session, sql)

    print("\nQuery Result:\n", result)

    session.close()


if __name__ == "__main__":
    test()
