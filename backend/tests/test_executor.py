import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from datetime import date, datetime
from core.executor import serialize_value, serialize_row, execute_sql_query, get_sample_data

def test_serialize_value():
    assert serialize_value(Decimal("10.5")) == 10.5
    assert serialize_value(date(2023, 1, 1)) == "2023-01-01"
    assert serialize_value(datetime(2023, 1, 1, 12, 0, 0)) == "2023-01-01T12:00:00"
    assert serialize_value("string") == "string"
    assert serialize_value(100) == 100

def test_serialize_row():
    row = {"price": Decimal("100.00"), "date": date(2023, 5, 20), "name": "Test"}
    serialized = serialize_row(row)
    assert serialized["price"] == 100.0
    assert serialized["date"] == "2023-05-20"
    assert serialized["name"] == "Test"

def test_execute_sql_query_success(mock_db_session):
    mock_result = MagicMock()
    mock_result.mappings().fetchall.return_value = [{"id": 1, "name": "Item 1"}]
    mock_db_session.execute.return_value = mock_result
    
    result = execute_sql_query(mock_db_session, "SELECT * FROM table")
    
    assert result["status"] == "success"
    assert len(result["data"]) == 1
    assert result["data"][0]["name"] == "Item 1"

def test_execute_sql_query_error(mock_db_session):
    mock_db_session.execute.side_effect = Exception("DB Error")
    
    result = execute_sql_query(mock_db_session, "INVALID SQL")
    
    assert result["status"] == "error"
    assert "DB Error" in result["message"]

@patch("core.executor.os.path.exists")
@patch("core.executor.open", create=True)
def test_get_sample_data_from_file(mock_open, mock_exists):
    mock_exists.return_value = True
    mock_file = MagicMock()
    mock_file.read.return_value = '[{"id": 1, "name": "Laptop"}]'
    mock_open.return_value.__enter__.return_value = mock_file
    
    result = get_sample_data()
    
    assert len(result) == 1
    assert result[0]["name"] == "Laptop"
