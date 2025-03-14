from app.database import Model, BaseModel, Theme

def test_theme_model():
  assert isinstance(Theme(), Model)
  assert isinstance(Theme(), BaseModel)
  
def test_theme_name_validator_with_valid_theme():
  valid_theme_names = ["Code quality", "Meeting user needs", "The CI-CD pipeline", "Refreshing and patching", "Operability", "Data persistence", "Automation", "Data security"]

  for name in valid_theme_names:
    theme = Theme(id="acde070d-8c4c-4f0d-9d8a-162843c10333", theme_name = name)
    theme.theme_name_validator()
    assert theme.theme_name == name 
