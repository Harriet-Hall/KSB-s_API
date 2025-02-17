import pytest
from peewee import *
from database import Ksb, BaseModel
import os

psql_test_db = PostgresqlDatabase(
    os.getenv("TEST_DATABASE"),
    host=os.getenv("TEST_HOST"),
    user=os.getenv("TEST_USER"),
    password=os.getenv("TEST_PASSWORD"),
    port=os.getenv("TEST_PORT")
)

     
@pytest.fixture(scope="function")
def test_database():
    psql_test_db.bind([Ksb])
    psql_test_db.connect()
    with psql_test_db.transaction() as transaction:
        try:     
            yield transaction 
        finally: 
            transaction.rollback()
    psql_test_db.close()

def test_Ksb_model():  
    Ksb_instance = Ksb()
    assert isinstance(Ksb_instance, Model)
    assert isinstance(Ksb_instance, BaseModel)


def test_table_is_seeded(test_database):
        rows = Ksb.select()
        assert len(rows) == 4
        

def test_insert_entry_into_table(test_database):

    Ksb.create(
        ksb_type= "Knowledge",
        ksb_code= 1,
        description="Test description",
    )
    
    rows = Ksb.select()
    assert len(rows) == 5

    new_row = rows[-1]
    assert new_row.id 
    assert new_row.ksb_type == "Knowledge"
    assert new_row.ksb_code == 1
    assert new_row.description == "Test description"
