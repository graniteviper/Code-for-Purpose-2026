import pytest
from unittest.mock import MagicMock, patch
from core.get_sql_from_llm import SQLGenerator, validate_sql, build_sql_prompt

def test_validate_sql():
    assert validate_sql("SELECT * FROM inventory") is True
    assert validate_sql("select name from products") is True
    assert validate_sql("DROP TABLE inventory") is False
    assert validate_sql("DELETE FROM inventory") is False
    assert validate_sql("UPDATE inventory SET qty=0") is False
    assert validate_sql("INSERT INTO inventory VALUES (...)") is False
    assert validate_sql("SHOW TABLES") is False  # Doesn't start with SELECT

def test_build_sql_prompt():
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
    mock_get_sample.return_value = []
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "```sql\nSELECT * FROM inventory\n```"
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model
    
    generator = SQLGenerator()
    sql = generator.generate_sql("query", {}, "schema")
    
    assert sql == "SELECT * FROM inventory"
    mock_model.generate_content.assert_called_once()
