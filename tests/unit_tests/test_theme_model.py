from app.database import Model, BaseModel, Theme

def test_theme_model():
  assert isinstance(Theme(), Model)
  assert isinstance(Theme(), BaseModel)