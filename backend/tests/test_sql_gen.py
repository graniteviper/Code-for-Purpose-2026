import pytest
from unittest.mock import MagicMock, patch
from core.get_sql_from_llm import SQLGenerator, validate_sql, build_sql_prompt

"""
Unit tests for the SQL generation module.
Covers SQL safety validation, prompt construction logic, and the 
SQLGenerator service's interaction with the Gemini API.
"""

def test_validate_sql():
    """
    Verifies the read-only safety filter for generated SQL.
    Only SELECT statements (case-insensitive) are allowed.
    """
    # Safe queries
    assert validate_sql("SELECT * FROM inventory") is True
    assert validate_sql("select name from products") is True
    
    # Destructive/Unsafe queries
    assert validate_sql("DROP TABLE inventory") is False
    assert validate_sql("DELETE FROM inventory") is False
    assert validate_sql("UPDATE inventory SET qty=0") is False
    assert validate_sql("INSERT INTO inventory VALUES (...)") is False
    assert validate_sql("SHOW TABLES") is False  # Restricted for security reasons

def test_build_sql_prompt():
    """
    Ensures that the final prompt sent to the LLM contains all critical context:
    1. The original user query
    2. The relevant DB schema
    3. Sample data for better column interpretation
    """
    user_query = "What are the laptop sales?"
    parsed_json = {"category": "summary"}
    db_schema = "table inventory(product_name, revenue)"
    sample_rows = [{"product_name": "Laptop", "revenue": 100}]
    
    prompt = build_sql_prompt(user_query, parsed_json, db_schema, sample_rows)
    
    assert "What are the laptop sales?" in prompt
    assert "inventory" in prompt
    assert "Laptop" in prompt

@patch("core.get_sql_from_llm.genai.GenerativeModel")
@patch("core.get_sql_from_llm.get_sample_data")
def test_sql_generator_generate(mock_get_sample, mock_model_class):
    """
    Tests the main SQL generation flow by mocking the LLM's raw output.
    Ensures that markdown code blocks (```sql) are correctly stripped from the result.
    """
    mock_get_sample.return_value = [] # Assume no sample data for this test
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "```sql\nSELECT * FROM inventory\n```"
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    generator = SQLGenerator()
    sql = generator.generate_sql("query", {}, "schema")
    
    # Verify the SQL is correctly extracted and stripped
    assert sql == "SELECT * FROM inventory"
    mock_model.generate_content.assert_called_once()
