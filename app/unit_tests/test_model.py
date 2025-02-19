import pytest
from database import Ksb, Model, BaseModel

def test_Ksb_model():  
    Ksb_instance = Ksb()
    assert isinstance(Ksb_instance, Model)
    assert isinstance(Ksb_instance, BaseModel)
    
def test_ksb_properties_have_correct_types():
  ksb = Ksb(id = "acde070d-8c4c-4f0d-9d8a-162843c10333", ksb_type = "knowledge", ksb_code = 1, description = "Test description")
  assert isinstance(ksb.id, str)
  assert isinstance(ksb.ksb_type, str)
  assert isinstance(ksb.ksb_code, int)
  assert isinstance(ksb.description, str)
  
  
def test_ksb_type_validator():
  ksb_type_values = ['Knowledge', 'knowledge', 'Skill', 'skill', 'Behaviour', 'behaviour']

  for i, ksb_type_value in enumerate(ksb_type_values):
    ksb = Ksb(id = "acde070d-8c4c-4f0d-9d8a-162843c10333", ksb_type = ksb_type_value, ksb_code = 1, description = "Test description")
    ksb.ksb_type_validator()
    assert ksb.ksb_type == ksb_type_values[i].capitalize()
  
  
def test_error_raised_if_ksb_type_is_invalid():
    with pytest.raises(ValueError) as value_error:      
      ksb = Ksb(id = "acde070d-8c4c-4f0d-9d8a-162843c10123", ksb_type = "behave", ksb_code = 2, description = "Test description")
      ksb.ksb_type_validator()
      assert value_error.value == f"{ksb.ksb_type} is not a valid ksb_type"
    
  
def test_ksb_type_first_letter_is_capitalised():
    ksb = Ksb(id = "acde070d-8c4c-4f0d-9d8a-162843c10123", ksb_type = "skill", ksb_code = 2, description = "Test description")
    ksb.ksb_type_validator()
    assert ksb.ksb_type == "Skill"
  
def test_save_calls_ksb_type_validator():
    ksb = Ksb(id = "acde070d-8c4c-4f0d-9d8a-162843c10456", ksb_type = "behaviour", ksb_code = 3, description = "Test description")
    ksb.save()
    assert ksb.ksb_type == "Behaviour"