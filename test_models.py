from peewee import *
from app import Ksb, BaseModel

def test_Ksb_model():
    Ksb_instance = Ksb()
    assert isinstance(Ksb_instance, Model)
    assert isinstance(Ksb_instance, BaseModel)
