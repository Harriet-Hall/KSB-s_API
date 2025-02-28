from app.database import Ksb
import pytest
from peewee import PostgresqlDatabase
import os

psql_test_db = PostgresqlDatabase(
    os.getenv("DATABASE"),
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
