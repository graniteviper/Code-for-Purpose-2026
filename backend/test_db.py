from sqlalchemy import text
from core.database import get_db_session

def test_connection():
    try:
        # get_db_session is a generator, so we use next() to get the actual session
        session = next(get_db_session())
        
        # Execute a simple query
        result = session.execute(text("SELECT 1 AS test_connection;")).fetchone()
        
        print("\n✅ SUCCESS: Connection to Neon DB established!")
        print(f"✅ DB Response: {result._mapping}\n")
        
    except ValueError as e:
        print(f"\n❌ SETUP ERROR: {e}")
        print("Did you forget to create the .env file with your DATABASE_URL?\n")
    except Exception as e:
        print(f"\n❌ CONNECTION ERROR: Failed to connect to the database.")
        print(f"Details: {e}\n")

if __name__ == "__main__":
    test_connection()
