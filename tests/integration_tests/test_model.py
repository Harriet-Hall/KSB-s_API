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



def test_table_is_seeded(test_database):
        rows = Ksb.select()
        assert len(rows) == 4
        

def test_create_ksb_entry(test_database):

    Ksb.create(
        ksb_type= "Knowledge",
        ksb_code= 1,
        description="Test description"
    )
    
    rows = Ksb.select()
    assert len(rows) == 5

    new_row = rows[4]
    assert new_row.id 
    assert new_row.ksb_type == "Knowledge" and isinstance(new_row.ksb_type, str)
    assert new_row.ksb_code == 1 and isinstance(new_row.ksb_code, int)
    assert new_row.description == "Test description" and isinstance(new_row.description, str)
    


def test_create_ksb_entry_with_valid_ksb_types(test_database):
    ksb_type_values = ['Knowledge', 'knowledge', 'Skill', 'skill', 'Behaviour', 'behaviour']
    for ksb_type_value in ksb_type_values:
        Ksb.create(
        ksb_type=f"{ksb_type_value}",
        ksb_code= 1,
        description="Test description"
        )
    rows = Ksb.select()

    assert len(rows) == 10
    new_rows = rows[4:]
    for i, row in enumerate(new_rows):
        assert row.ksb_type == ksb_type_values[i].capitalize()

    
    
def test_ksb_types_first_letter_is_capitalised(test_database):
    Ksb.create(
    ksb_type= "knowledge",
    ksb_code= 1,
    description="Test description"
)

    rows = Ksb.select()
    assert rows[4].ksb_type == "Knowledge"
    
def test_error_raised_when_ksb_type_is_invalid(test_database):
    with pytest.raises(ValueError) as value_error:
        Ksb.create(
        ksb_type= "ski1111",
        ksb_code= 1,
        description="Test description"
    )
        assert value_error.value == "ski1111 is not a valid ksb_type"
        

def test_create_ksb_entry_with_valid_ksb_code(test_database):
        Ksb.create(
        ksb_type="knowledge",
        ksb_code= 1,
        description="Test description",
        )
        row = Ksb.select()
        assert row[4].ksb_code == 1

def test_create_ksb_entry_with_invalid_ksb_code(test_database):
    with pytest.raises(ValueError) as value_error:

        invalid_codes = ["3", 788, 7,3]
        for code in invalid_codes:
            
            Ksb.create(
            ksb_type="knowledge",
            ksb_code=code,
            description="Test description"
            )
        
        assert value_error.value == f"{code} is not a valid ksb_code, choose an integer from 1 to 50"    


def test_create_ksb_entry_with_valid_ksb_description(test_database):
        Ksb.create(
        ksb_type="knowledge",
        ksb_code= 1,
        description="Test description",
        )
        row = Ksb.select()
        assert row[4].description == "Test description"
    
def test_create_ksb_entry_with_invalid_ksb_description(test_database):
    with pytest.raises(ValueError) as value_error:
    
            Ksb.create(
            ksb_type="knowledge",
            ksb_code="Too short",
            description="Test description"
            )
    assert str(value_error.value) == "Too short is not a valid ksb_code, choose a int from 1 to 25"
