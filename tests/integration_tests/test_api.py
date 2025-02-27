from base64 import decode
from ...app.app import app
import json
from ...app.database import Ksb
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
    os.getenv("POSTGRES_DATABASE"),
    host=os.getenv("POSTGRES_HOST"),
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=os.getenv("POSTGRES_PORT"),
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


def test_get_request_to_invalid_endpoint_returns_error(mock_client, test_database):
    response = mock_client.get("/behavir")
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data["error"] == "endpoint does not exist"


def test_post_a_ksb_to_home_endpoint(mock_client, test_database):
    data = {"ksb_type": "Knowledge", "ksb_code": 12, "description": "Test description"}
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
    assert (
        response_data["error"]
        == "100 is not a valid ksb_code, choose an int from 1 to 50"
    )


def test_delete_ksb(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_delete = ksbs[0]

    response = mock_client.delete(f"/{ksb_to_delete.id}")
    assert response.status_code == 204
    assert len(Ksb.select()) == 3


def test_delete_ksb_that_does_not_exist_in_database(mock_client, test_database):

    response = mock_client.delete(f"/acde070d-8c4c-4f0d-9d8a-162843c10333")
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert (
        response_data["error"]
        == "ksb cannot be deleted as it does not exist in database"
    )

    assert len(Ksb.select()) == 4


def test_delete_ksb_with_invalid_data_returns_an_error(mock_client, test_database):

    response = mock_client.delete(f"/123")
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data["error"] == "uuid is invalid"

    assert len(Ksb.select()) == 4


def test_update_ksb(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_update = ksbs[0]

    assert ksb_to_update.ksb_type == "Knowledge"
    assert ksb_to_update.ksb_code == 5
    assert (
        ksb_to_update.description
        == "Modern security tools and techniques, including threat modelling and vulnerability scanning."
    )

    data = {
        "ksb_type": "Skill",
        "ksb_code": 6,
        "description": "Install, manage and troubleshoot monitoring tools",
    }
    response = mock_client.put(f"/{ksb_to_update.id}", json=data)

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["type"] == data["ksb_type"]
    assert response_data["code"] == data["ksb_code"]
    assert response_data["description"] == data["description"]

    updated_ksb = Ksb.get(Ksb.id == ksb_to_update.id)

    assert updated_ksb.ksb_type == "Skill"
    assert updated_ksb.ksb_code == 6
    assert (
        updated_ksb.description == "Install, manage and troubleshoot monitoring tools"
    )
    assert len(Ksb.select()) == 4


def test_update_ksb_with_valid_uuid_but_ksb_does_not_exist_in_database(
    mock_client, test_database
):

    data = {
        "ksb_type": "Skill",
        "ksb_code": 6,
        "description": "Install, manage and troubleshoot monitoring tools",
    }
    response = mock_client.put(f"/acde070d-8c4c-4f0d-9d8a-162843c10333", json=data)
    assert response.status_code == 404
    


def test_update_ksb_with_invalid_uuid(mock_client, test_database):

    data = {
        "ksb_type": "Skill",
        "ksb_code": 6,
        "description": "Install, manage and troubleshoot monitoring tools",
    }
    response = mock_client.put(f"/123", json=data)
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data["error"] == "uuid is invalid"

    assert len(Ksb.select()) == 4


def test_update_ksb_type(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_update = ksbs[0]
    assert ksb_to_update.ksb_type == "Knowledge"
    assert ksb_to_update.ksb_code == 5
    assert (
        ksb_to_update.description
        == "Modern security tools and techniques, including threat modelling and vulnerability scanning."
    )

    data = {
        "ksb_type": "Skill",
    }
    response = mock_client.put(f"/{ksb_to_update.id}", json=data)

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["type"] == "Skill"

    updated_ksb = Ksb.get(Ksb.id == ksb_to_update.id)

    assert updated_ksb.ksb_type == "Skill"
    assert updated_ksb.ksb_code == 5
    assert (
        updated_ksb.description
        == "Modern security tools and techniques, including threat modelling and vulnerability scanning."
    )
    
def test_update_ksb_with_invalid_ksb_type(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_update = ksbs[0]
    assert ksb_to_update.ksb_type == "Knowledge"

    data = {"ksb_type": "ski1111"}
    response = mock_client.put(f"/{ksb_to_update.id}", json=data)
    assert response.status_code == 400
    response_data = json.loads(response.data)

    assert response_data["error"] == "Ski1111 is not a valid ksb_type"
    
    
def test_update_ksb_code(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_update = ksbs[0]
    assert ksb_to_update.ksb_type == "Knowledge"
    assert ksb_to_update.ksb_code == 5
    assert (
        ksb_to_update.description
        == "Modern security tools and techniques, including threat modelling and vulnerability scanning."
    )

    data = {
        "ksb_code": 4,
    }
    response = mock_client.put(f"/{ksb_to_update.id}", json=data)

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["code"] == 4

    updated_ksb = Ksb.get(Ksb.id == ksb_to_update.id)

    assert updated_ksb.ksb_type == "Knowledge"
    assert updated_ksb.ksb_code == 4
    assert (
        updated_ksb.description
        == "Modern security tools and techniques, including threat modelling and vulnerability scanning."
    )


def test_update_ksb_with_invalid_ksb_code(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_update = ksbs[0]
    assert ksb_to_update.ksb_code == 5

    data = {"ksb_code": 2.2}
    response = mock_client.put(f"/{ksb_to_update.id}", json=data)
    assert response.status_code == 400
    response_data = json.loads(response.data)

    assert response_data["error"] == "2.2 is of type: float, it needs to be an integer"


def test_update_ksb_description(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_update = ksbs[1]
    assert ksb_to_update.ksb_type == "Knowledge"
    assert ksb_to_update.ksb_code == 7
    assert (
        ksb_to_update.description
        == "General purpose programming and infrastructure-as-code."
    )

    data = {
        "description": "updated description",
    }
    response = mock_client.put(f"/{ksb_to_update.id}", json=data)

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["description"] == "updated description"

    updated_ksb = Ksb.get(Ksb.id == ksb_to_update.id)

    assert updated_ksb.ksb_type == "Knowledge"
    assert updated_ksb.ksb_code == 7
    assert updated_ksb.description == "updated description"

def test_update_ksb_description_with_invalid_description(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_update = ksbs[0]
    assert ksb_to_update.ksb_code == 5

    data = {"description": ""}
    response = mock_client.put(f"/{ksb_to_update.id}", json=data)

    assert response.status_code == 400
    response_data = json.loads(response.data)

    assert response_data["error"] == "description needs to be more than 15 characters and less than 300 characters in length"
    