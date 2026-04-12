import pytest
from unittest.mock import patch, MagicMock

def test_root_endpoint(client):
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
    # Setup mocks
    mock_plan.return_value = {"category": "summary", "note": "test note"}
    mock_get_schema.return_value = {"tables": []}
    
    mock_sql_gen = MagicMock()
    mock_sql_gen.generate_sql.return_value = "SELECT 1"
    mock_sql_gen_class.return_value = mock_sql_gen
    
    mock_execute.return_value = {"status": "success", "data": [{"result": 1}]}
    
    mock_explainer = MagicMock()
    mock_explainer.generate.return_value = "This is an explanation."
    mock_explainer_class.return_value = mock_explainer
    
    # Request
    payload = {"query": "test query"}
    response = client.post("/query", json=payload)
    
    # Assertions
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
    mock_validate.return_value = False
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
    mock_sql_gen = MagicMock()
    mock_sql_gen.generate_sql.return_value = "SELECT * FROM non_existent"
    mock_sql_gen_class.return_value = mock_sql_gen
    
    mock_execute.return_value = {"status": "error", "message": "Table not found"}
    
    payload = {"query": "fail query"}
    response = client.post("/query", json=payload)
    
    assert response.status_code == 200
    assert "error" in response.json()
    assert "Failed to execute SQL" in response.json()["error"]
