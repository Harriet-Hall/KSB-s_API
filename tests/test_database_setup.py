from app.database import Ksb
import pytest
from peewee import PostgresqlDatabase
import os

test_db = PostgresqlDatabase(
    "postgres",
    host="test_db",
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=5432
)

@pytest.fixture
def test_database():
    test_db.bind([Ksb])
    test_db.connect()
    with test_db.transaction() as transaction:
        try:
            yield transaction
        finally:
            transaction.rollback()
    test_db.close()
