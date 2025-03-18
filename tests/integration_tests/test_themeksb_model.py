import pytest
from peewee import *
from app.database import Theme, Ksb, ThemeKsb, psql_db
import os
os.environ["ENVIRONMENT"] = "test"


@pytest.fixture(scope="function")
def test_database():
    psql_db.bind([Theme, Ksb, ThemeKsb])
    psql_db.connect()
    with psql_db.transaction() as transaction:
        try:
            yield transaction
        finally:
            transaction.rollback()
    psql_db.close()


def test_table_is_created_with_correct_properties(test_database):
    data = (
        ('Code Quality', [
            { 'ksb_type': 'Knowledge', 'ksb_code': 11, 'description': 'description for this ksb is ...'},
            { 'ksb_type': 'Skill', 'ksb_code': 12, 'description': 'description for this ksb is ...'},
            { 'ksb_type': 'Behaviour', 'ksb_code': 13, 'description': 'description for this ksb is ...'}
        ]),
        ('Operability', [
            { 'ksb_type': 'Knowledge', 'ksb_code': 21, 'description': 'description for this ksb is ...'},
            {'ksb_type': 'Skill', 'ksb_code': 22, 'description': 'description for this ksb is ...'},
            {'ksb_type': 'Behaviour', 'ksb_code': 23, 'description': 'Odescription for this ksb is ...'}
        ])
    )
    for theme_name, ksbs in data:
        theme = Theme.create(theme_name = theme_name) 

        for ksb_data in ksbs:
            ksb = Ksb.create(
               
                ksb_type=ksb_data['ksb_type'],
                ksb_code=ksb_data['ksb_code'],
                description=ksb_data['description']
            )
           
            ThemeKsb.create(theme_id=theme.id, ksb_id=ksb.id)
      