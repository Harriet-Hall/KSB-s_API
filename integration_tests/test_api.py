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
    port=os.getenv("TEST_PORT"),
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


def test_get_request_to_knowledge_endpoint_returns_200(mock_client, test_database):
    response = mock_client.get("/knowledge")
    assert response.status_code == 200


def test_get_request_to_knowledge_endpoint_returns_list_of_knowledge_ksbs(
    mock_client, test_database
):
    response = mock_client.get("/knowledge")
    response_data = json.loads(response.data)
    assert len(response_data) == 2
    for ksb in response_data:
        assert ksb["type"] == "Knowledge"


def test_get_request_to_skill_endpoint_returns_list_of_skill_ksbs(
    mock_client, test_database
):
    response = mock_client.get("/skill")
    response_data = json.loads(response.data)
    assert len(response_data) == 1
    for ksb in response_data:
        assert ksb["type"] == "Skill"


def test_get_request_to_behaviour_endpoint_returns_list_of_behaviour_ksbs(
    mock_client, test_database
):
    response = mock_client.get("/behaviour")
    response_data = json.loads(response.data)
    assert len(response_data) == 1
    for ksb in response_data:
        assert ksb["type"] == "Behaviour"


def test_post_a_ksb_to_home_endpoint(mock_client, test_database):
    data = {
        "ksb_type": "Knowledge",
        "ksb_code": 12,
        "description": "Test description"
    }
    response = mock_client.post("/", json=data)
    assert response.status_code == 201
    response_data = json.loads(response.data)
    assert len(str(response_data["id"])) == 36
    assert response_data["type"] == "Knowledge"
    assert response_data["code"] == 12
    assert response_data["description"] == "Test description"
    
def test_post_a_ksb_to_home_endpoint_that_already_exists(mock_client, test_database):
    data = {
        "ksb_type": "Skill",
        "ksb_code": 9,
        "description": "Using cloud security tools and automating security in pipelines.",
    }
    response = mock_client.post("/", json=data)
    assert response.status_code == 409
    response_data = json.loads(response.data)
    assert response_data["error"] == "Ksb already exists in database"
    assert len(Ksb.select()) == 4
    
def test_post_ksb_with_invalid_ksb_type(mock_client, test_database):
    data = {
        "ksb_type": "invalid",
        "ksb_code": 10,
        "description": "Assess identified and potential security threats and take appropriate action based on likelihood v impact.",
    }
    response = mock_client.post("/", json=data)
    assert response.status_code == 400
    response_data = json.loads(response.data)
    print(response_data)
    assert response_data["error"] == "invalid is not a valid ksb_type"
    
    
def test_post_ksb_with_invalid_ksb_code(mock_client, test_database):
    data = {
        "ksb_type": "behaviour",
        "ksb_code": 100,
        "description": "Assess identified and potential security threats and take appropriate action based on likelihood v impact.",
    }
    response = mock_client.post("/", json=data)
    assert response.status_code == 400
    response_data = json.loads(response.data)
    print(response_data)
    assert response_data["error"] == "100 is not a valid ksb_code, choose a number from 1 to 25"
    
    
    