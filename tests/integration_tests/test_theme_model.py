import uuid
import pytest
from peewee import *
from app.database import Theme, psql_db
import os

os.environ["ENVIRONMENT"] = "test"


@pytest.fixture(scope="function")
def test_database():
    psql_db.bind([Theme])
    psql_db.connect()
    with psql_db.transaction() as transaction:
        try:
            yield transaction
        finally:
            transaction.rollback()
    psql_db.close()


def test_table_is_seeded(test_database):
    rows = Theme.select()
    assert len(rows) == 8


def test_table_contains_correct_data(test_database):
    rows = Theme.select()
    row = rows[0]
    assert isinstance(row.id, uuid.UUID)
    assert row.theme_name == "code quality"
