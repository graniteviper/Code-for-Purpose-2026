import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
from core.database import get_db_session

# Pytest Configuration and Shared Fixtures
# This file contains reusable fixtures for the backend test suite.

@pytest.fixture
def mock_db_session():
    """
    Fixture to provide a mocked SQLAlchemy session.
    Using a MagicMock avoids the need for a live database connection during unit tests.
    """
    session = MagicMock()
    return session

@pytest.fixture
def client(mock_db_session):
    """
    Fixture to provide a FastAPI TestClient with a mocked database dependency.
    This allows testing API endpoints in isolation by swapping the real DB session
    with the 'mock_db_session' fixture.
    """
    def override_get_db():
        try:
            yield mock_db_session
        finally:
            pass
    
    # Override the get_db_session dependency in the FastAPI application
    app.dependency_overrides[get_db_session] = override_get_db
    
    with TestClient(app) as c:
        yield c
        
    # Clear overrides after each test to prevent leaking state between tests
    app.dependency_overrides.clear()
