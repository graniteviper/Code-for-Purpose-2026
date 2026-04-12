import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app
from core.database import get_db_session

@pytest.fixture
def mock_db_session():
    """Fixture to provide a mocked SQLAlchemy session."""
    session = MagicMock()
    return session

@pytest.fixture
def client(mock_db_session):
    """Fixture to provide a FastAPI TestClient with overridden DB dependency."""
    def override_get_db():
        try:
            yield mock_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db_session] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
