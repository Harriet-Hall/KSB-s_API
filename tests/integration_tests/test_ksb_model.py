import uuid
from datetime import datetime
import pytest
from peewee import *
from app.database import Ksb, psql_db
import os
os.environ["ENVIRONMENT"] = "test"


@pytest.fixture(scope="function")
def test_database():
    psql_db.bind([Ksb])
    psql_db.connect()
    with psql_db.transaction() as transaction:
        try:
            yield transaction
        finally:
            transaction.rollback()
    psql_db.close()


def test_table_is_seeded(test_database):
    rows = Ksb.select()
    assert len(rows) == 4


def test_table_contains_correct_data(test_database):
    rows = Ksb.select()
    row = rows[0]
    assert isinstance(row.id, uuid.UUID)
    assert isinstance(row.ksb_type, str)
    assert isinstance(row.ksb_code, int)
    assert isinstance(row.description, str)
    assert isinstance(row.created_at, datetime)
    assert isinstance(row.updated_at, datetime)

def test_create_ksb_entry(test_database):

    Ksb.create(ksb_type="Knowledge", ksb_code=1, description="Test description")

    rows = Ksb.select()
    assert len(rows) == 5

    new_row = rows[4]
    assert new_row.id
    assert new_row.ksb_type == "Knowledge" and isinstance(new_row.ksb_type, str)
    assert new_row.ksb_code == 1 and isinstance(new_row.ksb_code, int)
    assert new_row.description == "Test description" and isinstance(
        new_row.description, str
    )


def test_create_ksb_entry_with_valid_ksb_types(test_database):
    ksb_type_values = [
        "Knowledge",
        "knowledge",
        "Skill",
        "skill",
        "Behaviour",
        "behaviour",
    ]
    for ksb_type_value in ksb_type_values:
        Ksb.create(
            ksb_type=f"{ksb_type_value}", ksb_code=1, description="Test description"
        )
    rows = Ksb.select()

    assert len(rows) == 10
    new_rows = rows[4:]
    for i, row in enumerate(new_rows):
        assert row.ksb_type == ksb_type_values[i].capitalize()


def test_error_raised_when_ksb_type_is_invalid(test_database):

    with pytest.raises(ValueError) as value_error:
        invalid_types = ["", 123, "ski1111"]
        for type in invalid_types:

            Ksb.create(ksb_type=type, ksb_code=1, description="Test description")

    assert str(value_error.value) == f"{type} is not a valid ksb_type"


def test_create_ksb_entry_with_valid_ksb_code(test_database):
    Ksb.create(
        ksb_type="knowledge",
        ksb_code=1,
        description="Test description",
    )
    row = Ksb.select()
    assert row[4].ksb_code == 1


def test_create_ksb_entry_with_invalid_ksb_code_string(test_database):
    with pytest.raises(ValueError) as value_error:
        Ksb.create(ksb_type="knowledge", ksb_code="3", description="Test description")
    assert str(value_error.value) == "3 is of type: str, it needs to be an integer"


def test_create_ksb_entry_with_invalid_ksb_code_out_of_range_low(test_database):
    with pytest.raises(ValueError) as value_error:
        Ksb.create(ksb_type="knowledge", ksb_code=0, description="Test description")
    assert (
        str(value_error.value)
        == "0 is not a valid ksb code, choose an int from 1 to 50"
    )


def test_create_ksb_entry_with_invalid_ksb_code_out_of_range_high(test_database):
    with pytest.raises(ValueError) as value_error:
        Ksb.create(ksb_type="knowledge", ksb_code=51, description="Test description")
    assert (
        str(value_error.value)
        == "51 is not a valid ksb code, choose an int from 1 to 50"
    )


def test_create_ksb_entry_with_invalid_ksb_code_empty_string(test_database):
    with pytest.raises(ValueError) as value_error:
        Ksb.create(ksb_type="knowledge", ksb_code="", description="Test description")
    assert str(value_error.value) == " is of type: str, it needs to be an integer"


def test_create_ksb_entry_with_valid_ksb_description(test_database):
    Ksb.create(
        ksb_type="knowledge",
        ksb_code=1,
        description="Test description",
    )
    row = Ksb.select()
    assert row[4].description == "Test description"


def test_create_ksb_entry_with_invalid_ksb_description(test_database):

    with pytest.raises(ValueError) as value_error:
        invalid_descriptions = ["Too short", ("i" * 301), ""]
        for description in invalid_descriptions:

            Ksb.create(ksb_type="knowledge", ksb_code=12, description=description)
    assert (
        str(value_error.value)
        == "description needs to be more than 15 characters and less than 300 characters in length"
    )
