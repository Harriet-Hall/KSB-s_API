from app.app import app
import json
import os
from app.database import Ksb, Theme, ThemeKsb, psql_db

import pytest
os.environ["ENVIRONMENT"] = "test"

@pytest.fixture
def test_app():
    yield app


@pytest.fixture
def mock_client(test_app):
    return test_app.test_client()


@pytest.fixture
def test_database():
    psql_db.bind([Ksb])
    psql_db.connect()
    with psql_db.transaction() as transaction:
        try:
            yield transaction
        finally:
            transaction.rollback()
    psql_db.close()


def test_get_request_to_ksbs_endpoint_returns_200(mock_client, test_database):
    response = mock_client.get("/ksbs")
    assert response.status_code == 200


def test_get_request_to_ksbs_endpoint_returns_list_of_ksbs(mock_client, test_database):
    response = mock_client.get("/ksbs")
    response_data = json.loads(response.data)
    assert len(response_data) == 4
    keys = response_data[0].keys()
    for key in keys:
        assert key in ["id", "type", "code", "description", "created_at", "updated_at", "theme", "is_complete"]

def test_get_request_to_ksbs_endpoint_returns_correct_theme_for_each_ksb(mock_client, test_database):
    response = mock_client.get("/ksbs")
    response_data = json.loads(response.data)
    for ksb in response_data:
        ksb_description = ksb["description"]
        ksb_theme = ksb["theme"]
    if ksb_description == "General purpose programming and infrastructure-as-code.":
        assert ksb_theme == "code quality"
    
def test_get_request_to_knowledge_endpoint_returns_200(mock_client, test_database):
    response = mock_client.get("/ksbs/knowledge")
    assert response.status_code == 200


def test_get_request_to_knowledge_endpoint_returns_list_of_knowledge_ksbs(
    mock_client, test_database
):
    response = mock_client.get("/ksbs/knowledge")
    response_data = json.loads(response.data)
    assert len(response_data) == 2
    for ksb in response_data:
        assert ksb["type"] == "Knowledge"


def test_get_request_to_skill_endpoint_returns_list_of_skill_ksbs(
    mock_client, test_database
):
    response = mock_client.get("/ksbs/skill")
    response_data = json.loads(response.data)
    assert len(response_data) == 1
    for ksb in response_data:
        assert ksb["type"] == "Skill"


def test_get_request_to_behaviour_endpoint_returns_list_of_behaviour_ksbs(
    mock_client, test_database
):
    response = mock_client.get("/ksbs/behaviour")
    response_data = json.loads(response.data)
    assert len(response_data) == 1
    for ksb in response_data:
        assert ksb["type"] == "Behaviour"


def test_get_request_to_invalid_endpoint_returns_error(mock_client, test_database):
    response = mock_client.get("/ksbs/behavir")
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data["error"] == "endpoint does not exist"


def test_post_a_ksb_to_correct_ksbs_type_endpoint(mock_client, test_database):
    data = {"code": 12, "description": "Test description", "theme": "meeting user needs"}
    response = mock_client.post("/ksbs/knowledge", json=data)
    
    assert response.status_code == 201
    response_data = json.loads(response.data)

    assert len(str(response_data["id"])) == 36
    assert response_data["type"] == "Knowledge"
    assert response_data["code"] == 12
    assert response_data["description"] == "Test description"
    assert response_data["theme"] == "meeting user needs"
    assert response_data["is_complete"] == False
    


def test_post_ksb_to_invalid_ksb_type_endpoint(mock_client, test_database):
    data = {
        "ksb_code": 10,
        "description": "Assess identified and potential security threats and take appropriate action based on likelihood v impact.",
        "theme": "meeting user needs"
    }
    response = mock_client.post("/ksbs/invalid", json=data)
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data["error"] == "endpoint does not exist"


def test_post_a_ksb_that_already_exists_returns_error(mock_client, test_database):
    data = {
        "code": 9,
        "description": "Using cloud security tools and automating security in pipelines.",
        "theme": "meeting user needs"
        
    }

    response = mock_client.post("/ksbs/skill", json=data)
    assert response.status_code == 409
    response_data = json.loads(response.data)
    assert response_data["error"] == "Some or all Ksb values already exists in database"
    assert len(Ksb.select()) == 4


def test_post_ksb_with_invalid_ksb_code(mock_client, test_database):
    data = {
        "code": 100,
        "description": "Assess identified and potential security threats and take appropriate action based on likelihood v impact.",
        "theme": "meeting user needs"
    }
    response = mock_client.post("/ksbs/Behaviour", json=data)
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert (
        response_data["error"]
        == "100 is not a valid ksb code, choose an int from 1 to 50"
    )
    
def test_post_ksb_with_invalid_ksb_description(mock_client, test_database):
    data = {
        "code": 10,
        "description": "",
        "theme": "code quality"
        
    }
    response = mock_client.post("/ksbs/Behaviour", json=data)
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert (
        response_data["error"]
        == "description needs to be more than 15 characters and less than 300 characters in length"
    )

def test_post_ksb_with_invalid_ksb_theme(mock_client, test_database):
    data = {
        "code": 10,
        "description": "Assess identified and potential security threats and take appropriate action based on likelihood v impact.",
        "theme": "invalid"
        
    }
    response = mock_client.post("/ksbs/Behaviour", json=data)
    assert response.status_code == 400
    response_data = json.loads(response.data)
    assert (
        response_data["error"]
        == "Invalid theme"
    )

def test_delete_ksb(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_delete = ksbs[0]

    response = mock_client.delete(f"/ksbs/{ksb_to_delete.id}")
    assert response.status_code == 204
    assert len(Ksb.select()) == 3
    
def test_delete_ksb_deletes_it_in_themeksb_table(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_delete = ksbs[0]

    mock_client.delete(f"/ksbs/{ksb_to_delete.id}")
    ksb = ThemeKsb.get_or_none(ksb_id = ksb_to_delete.id)
    assert ksb is None

def test_delete_ksb_that_does_not_exist_in_database(mock_client, test_database):

    response = mock_client.delete(f"/ksbs/acde070d-8c4c-4f0d-9d8a-162843c10333")
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert (
        response_data["error"]
        == "ksb cannot be deleted as it does not exist in database"
    )

    assert len(Ksb.select()) == 4


def test_delete_ksb_with_invalid_data_returns_an_error(mock_client, test_database):

    response = mock_client.delete(f"/ksbs/123")
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
        "type": "Skill",
        "code": 6,
        "description": "Install, manage and troubleshoot monitoring tools",
    }
    response = mock_client.put(f"/ksbs/{ksb_to_update.id}", json=data)

    assert response.status_code == 200
    response_data = json.loads(response.data)
    assert response_data["type"] == data["type"]
    assert response_data["code"] == data["code"]
    assert response_data["description"] == data["description"]

    updated_ksb = Ksb.get(Ksb.id == ksb_to_update.id)

    assert updated_ksb.ksb_type == "Skill"
    assert updated_ksb.ksb_code == 6
    assert (
        updated_ksb.description == "Install, manage and troubleshoot monitoring tools"
    )
    assert len(Ksb.select()) == 4

def test_update_ksb_is_complete_value(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_update = ksbs[0]
    data = {
        "is_complete": True
    }
    response = mock_client.put(f"/ksbs/{ksb_to_update.id}", json=data)
    response_data = json.loads(response.data)

    assert response_data["is_complete"] == True
    
def test_update_ksb_is_complete_with_invalid_value(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_update = ksbs[0]
    data = {
        "is_complete": "lll"
    }
    response = mock_client.put(f"/ksbs/{ksb_to_update.id}", json=data)
    response_data = json.loads(response.data)
    assert response_data["error"] == "is_complete must be a boolean (true or false)"
    

def test_update_ksb_with_valid_uuid_but_ksb_does_not_exist_in_database(
    mock_client, test_database
):

    data = {
        "ksb_type": "Skill",
        "ksb_code": 6,
        "description": "Install, manage and troubleshoot monitoring tools",
    }
    response = mock_client.put(f"/ksbs/acde070d-8c4c-4f0d-9d8a-162843c10333", json=data)
    assert response.status_code == 404
    response_data = json.loads(response.data)
    assert response_data["error"] == "ksb with that uuid does not exist in database"


def test_update_ksb_with_invalid_uuid(mock_client, test_database):

    data = {
        "ksb_type": "Skill",
        "ksb_code": 6,
        "description": "Install, manage and troubleshoot monitoring tools",
    }
    response = mock_client.put(f"/ksbs/123", json=data)
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
        "type": "Skill",
    }
    response = mock_client.put(f"/ksbs/{ksb_to_update.id}", json=data)

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

    data = {"type": "ski1111"}
    response = mock_client.put(f"/ksbs/{ksb_to_update.id}", json=data)
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
        "code": 4,
    }
    response = mock_client.put(f"/ksbs/{ksb_to_update.id}", json=data)

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

    data = {"code": 2.2}
    response = mock_client.put(f"/ksbs/{ksb_to_update.id}", json=data)
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
    response = mock_client.put(f"/ksbs/{ksb_to_update.id}", json=data)

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
    assert ksb_to_update.description == "Modern security tools and techniques, including threat modelling and vulnerability scanning."

    data = {"description": ""}
    response = mock_client.put(f"/ksbs/{ksb_to_update.id}", json=data)

    assert response.status_code == 400
    response_data = json.loads(response.data)

    assert response_data["error"] == "description needs to be more than 15 characters and less than 300 characters in length"

def test_updated_at_value_changes_when_ksb_is_updated(mock_client, test_database):
    ksbs = Ksb.select()
    ksb_to_update = ksbs[1]
    data = {
        "description": "updated description",
    }
    response = mock_client.put(f"/ksbs/{ksb_to_update.id}", json=data)
    response_data = json.loads(response.data)
    assert response_data["updated_at"] != ksb_to_update.updated_at
    
def test_get_request_to_theme_endpoint_returns_ksbs_for_that_theme(mock_client, test_database):
    response = mock_client.get("/ksbs/theme/code-quality")
    response_data = json.loads(response.data)
    assert len(response_data) == 2
    

def test_post_a_ksb_to_theme_endpoint(mock_client, test_database):
    ksbs = Ksb.select()
    ksb = ksbs[1]
    data = {"ksb_id": f"{ksb.id}"}
    theme = Theme.get(theme_name = "operability")
    response = mock_client.post("/ksbs/theme/operability", json=data)
    response_data = json.loads(response.data)
    

    assert response_data["ksb_id"] == str(ksb.id)
    assert response_data["theme_id"] == str(theme.id)