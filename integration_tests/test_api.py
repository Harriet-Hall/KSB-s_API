from app import app
from database import Ksb
import pytest


@pytest.fixture
def test_app():
    yield app

@pytest.fixture
def mock_client(test_app):
    return test_app.test_client()
        
def test_get_request_to_home_endpoint_returns_200(mock_client):
  response = mock_client.get("/")
  assert response.status_code == 200
