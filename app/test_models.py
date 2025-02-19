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
        

def test_create_ksb_entry(test_database):

    Ksb.create(
        ksb_type= "Knowledge",
        ksb_code= 1,
        description="Test description",
    )
    
    rows = Ksb.select()
    assert len(rows) == 5

    new_row = rows[4]
    assert new_row.id 
    assert new_row.ksb_type == "Knowledge" and isinstance(new_row.ksb_type, str)
    assert new_row.ksb_code == 1 and isinstance(new_row.ksb_code, int)
    assert new_row.description == "Test description" and isinstance(new_row.description, str)
    


def test_create_ksb_entry_with_valid_ksb_types(test_database):
    ksb_type_values = ['knowledge', 'skill', 'behaviour']
    for ksb_type_value in ksb_type_values:
        Ksb.create(
        ksb_type=f"{ksb_type_value}",
        ksb_code= 1,
        description="Test description",
        )
    rows = Ksb.select()

    assert len(rows) == 7
    assert rows[4].ksb_type == 'Knowledge'
    assert rows[5].ksb_type == 'Skill'
    assert rows[6].ksb_type == 'Behaviour'
    
    
def test_ksb_types_first_letter_is_capitalised(test_database):
    Ksb.create(
    ksb_type= "knowledge",
    ksb_code= 1,
    description="Test description",
)

    rows = Ksb.select()
    assert rows[4].ksb_type == "Knowledge"
    
def test_error_raised_when_ksb_type_is_invalid():
    with pytest.raises(ValueError) as value_error:
        Ksb.create(
        ksb_type= "ski1111",
        ksb_code= 1,
        description="Test description",
    )
        assert value_error.value == "ski1111 is not a valid ksb_type"
        
    