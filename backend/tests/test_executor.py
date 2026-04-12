import pytest
from unittest.mock import MagicMock, patch
from decimal import Decimal
from datetime import date, datetime
from core.executor import serialize_value, serialize_row, execute_sql_query, get_sample_data

"""
Unit tests for the database executor module.
Tests data serialization, SQL execution error handling, and sample data retrieval.
"""

def test_serialize_value():
    """
    Verifies that various non-JSON-serializable types (Decimal, Date) are
    correctly converted into their serializable counterparts.
    """
    assert serialize_value(Decimal("10.5")) == 10.5
    assert serialize_value(date(2023, 1, 1)) == "2023-01-01"
    assert serialize_value(datetime(2023, 1, 1, 12, 0, 0)) == "2023-01-01T12:00:00"
    assert serialize_value("string") == "string"
    assert serialize_value(100) == 100

def test_serialize_row():
    """
    Ensures that an entire row dictionary is correctly serialized.
    """
    row = {"price": Decimal("100.00"), "date": date(2023, 5, 20), "name": "Test"}
    serialized = serialize_row(row)
    assert serialized["price"] == 100.0
    assert serialized["date"] == "2023-05-20"
    assert serialized["name"] == "Test"

def test_execute_sql_query_success(mock_db_session):
    """
    Tests successful SQL execution by mocking the SQLAlchemy result object.
    """
    mock_result = MagicMock()
    mock_result.mappings().fetchall.return_value = [{"id": 1, "name": "Item 1"}]
    mock_db_session.execute.return_value = mock_result
    
    result = execute_sql_query(mock_db_session, "SELECT * FROM table")
    
    assert result["status"] == "success"
    assert len(result["data"]) == 1
    assert result["data"][0]["name"] == "Item 1"

def test_execute_sql_query_error(mock_db_session):
    """
    Tests error handling when the database engine throws an exception.
    """
    mock_db_session.execute.side_effect = Exception("DB Error")
    
    result = execute_sql_query(mock_db_session, "INVALID SQL")
    
    assert result["status"] == "error"
    assert "DB Error" in result["message"]
