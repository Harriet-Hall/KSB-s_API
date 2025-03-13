from app.database import Model, BaseModel, Theme

def test_theme_model():
  assert isinstance(Theme(), Model)
  assert isinstance(Theme(), BaseModel)
  
def test_theme_properties_have_correct_types():
  theme = Theme(
    id="acde070d-8c4c-4f0d-9d8a-162843c10333",
    theme_name="knowledge",
    created_at="Wed, 12 Mar 2025 12:45:39 GMT"
    )
  assert isinstance(theme.id, str)
  assert isinstance(theme.theme_name, str)
  assert isinstance(theme.created_at, str)
  