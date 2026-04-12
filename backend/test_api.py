from fastapi.testclient import TestClient
from main import app

"""
Manual API test script.
Used for quick verification of the /query endpoint during development.
Run with: python backend/test_api.py
"""

client = TestClient(app)
try:
    # Send a dummy query to the FastAPI test client
    response = client.post("/query", json={"query": "test"})
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.json()}")
except Exception as e:
    import traceback
    traceback.print_exc()
