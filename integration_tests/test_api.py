from app import app
import json
from database import Ksb
import pytest
from peewee import PostgresqlDatabase
import os

@pytest.fixture
def test_app():
    yield app

@pytest.fixture
def mock_client(test_app):
    return test_app.test_client()

psql_test_db = PostgresqlDatabase(
    os.getenv("TEST_DATABASE"),
    host=os.getenv("TEST_HOST"),
    user=os.getenv("TEST_USER"),
    password=os.getenv("TEST_PASSWORD"),
    port=os.getenv("TEST_PORT")
)

@pytest.fixture
def test_database():
    psql_test_db.bind([Ksb])
    psql_test_db.connect()
    with psql_test_db.transaction() as transaction:
        try:
            yield transaction
        finally:
            transaction.rollback()
    psql_test_db.close()
        

def test_get_request_to_home_endpoint_returns_200(mock_client):
  response = mock_client.get("/")
  assert response.status_code == 200

def test_get_request_to_home_endpoint_returns_list_of_ksbs(mock_client, test_database):
  response = mock_client.get("/")
  response_data = json.loads(response.data)
  assert len(response_data) == 4
  keys = response_data[0].keys()
  for key in keys:
    assert key in ["id", "type", "code", "description"]

def test_get_request_to_knowledge_endpoint_returns_list_of_knowledge_ksbs(mock_client, test_database):
  response = mock_client.get("/knowledge")
  response_data = json.loads(response.data)
  assert len(response_data) == 2
  for ksb in response_data:
      assert ksb["type"] == "Knowledge"
