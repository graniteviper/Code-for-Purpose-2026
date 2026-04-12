import pytest
from unittest.mock import MagicMock, patch
from core.schema_extractor import get_database_schema

@patch("core.schema_extractor.inspect")
@patch("core.schema_extractor.engine")
def test_get_database_schema(mock_engine, mock_inspect):
    mock_inspector = MagicMock()
    mock_inspect.return_value = mock_inspector
    
    mock_inspector.get_table_names.return_value = ["table1"]
    mock_inspector.get_view_names.return_value = ["view1"]
    mock_inspector.get_columns.side_effect = [
        [{"name": "col1", "type": "INT"}], # columns for table1
        [{"name": "col2", "type": "TEXT"}] # columns for view1
    ]
    
    schema = get_database_schema()
    
    assert "tables" in schema
    assert "views" in schema
    assert schema["tables"][0]["name"] == "table1"
    assert schema["tables"][0]["columns"][0]["name"] == "col1"
    assert schema["views"][0]["name"] == "view1"
    assert schema["views"][0]["columns"][0]["name"] == "col2"

@patch("core.schema_extractor.engine", None)
def test_get_database_schema_no_engine():
    schema = get_database_schema()
    assert "error" in schema
    assert "No database connection" in schema["error"]
