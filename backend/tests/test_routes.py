import pytest
from unittest.mock import patch, MagicMock

"""
Integration tests for the FastAPI routes.
Mocks all underlying core services (planner, generator, executor, explainer)
to verify the orchestration logic of the /query endpoint.
"""

def test_root_endpoint(client):
    """Verifies that the root health-check endpoint is reachable and returns the correct message."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API running 🚀"}

@patch("routes.query_routes.plan_query")
@patch("routes.query_routes.get_database_schema")
@patch("routes.query_routes.SQLGenerator")
@patch("routes.query_routes.execute_sql_query")
@patch("routes.query_routes.ExplanationGenerator")
def test_handle_query_success(
    mock_explainer_class,
    mock_execute,
    mock_sql_gen_class,
    mock_get_schema,
    mock_plan,
    client
):
    """
    Tests the happy path for the /query endpoint.
    Verifies that the pipeline correctly coordinates between the different services.
    """
    # Setup mocks for every step of the pipeline
    mock_plan.return_value = {"category": "summary", "note": "test note"}
    mock_get_schema.return_value = {"tables": []}
    
    mock_sql_gen = MagicMock()
    mock_sql_gen.generate_sql.return_value = "SELECT 1"
    mock_sql_gen_class.return_value = mock_sql_gen
    
    mock_execute.return_value = {"status": "success", "data": [{"result": 1}]}
    
    mock_explainer = MagicMock()
    mock_explainer.generate.return_value = "This is an explanation."
    mock_explainer_class.return_value = mock_explainer
    
    # Send the test request
    payload = {"query": "test query"}
    response = client.post("/query", json=payload)
    
    # Assert successful orchestration
    assert response.status_code == 200
    data = response.json()
    assert data["query"] == "test query"
    assert data["plan"]["category"] == "summary"
    assert data["sql"] == "SELECT 1"
    assert data["data"] == [{"result": 1}]
    assert data["explanation"] == "This is an explanation."

@patch("routes.query_routes.validate_sql")
@patch("routes.query_routes.SQLGenerator")
def test_handle_query_unsafe_sql(mock_sql_gen_class, mock_validate, client):
    """
    Verifies that the API blocks potentially destructive SQL commands.
    """
    mock_validate.return_value = False # Force validation failure
    mock_sql_gen = MagicMock()
    mock_sql_gen.generate_sql.return_value = "DROP TABLE students"
    mock_sql_gen_class.return_value = mock_sql_gen
    
    payload = {"query": "drop table"}
    response = client.post("/query", json=payload)
    
    assert response.status_code == 200
    assert "error" in response.json()
    assert response.json()["error"] == "Unsafe SQL generated"

@patch("routes.query_routes.execute_sql_query")
@patch("routes.query_routes.SQLGenerator")
def test_handle_query_execution_error(mock_sql_gen_class, mock_execute, client):
    """
    Ensures that database execution errors are gracefully returned to the user.
    """
    mock_sql_gen = MagicMock()
    mock_sql_gen.generate_sql.return_value = "SELECT * FROM non_existent"
    mock_sql_gen_class.return_value = mock_sql_gen
    
    mock_execute.return_value = {"status": "error", "message": "Table not found"}
    
    payload = {"query": "fail query"}
    response = client.post("/query", json=payload)
    
    assert response.status_code == 200
    assert "error" in response.json()
    assert "Failed to execute SQL" in response.json()["error"]
