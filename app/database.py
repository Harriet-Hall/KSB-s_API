import uuid
from peewee import *
import datetime
import os 
from .utils.ksb_type_choices import KSB_TYPE_CHOICES


psql_db = None
if os.getenv('ENVIRONMENT') == 'test':
  
  
   psql_db = PostgresqlDatabase( 
    "postgres",
    host="test_db",
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    port=5432
    )
   
else:

  from .secrets_manager import get_secret

  credentials = get_secret()

  database = credentials["DATABASE"]
  password = credentials["PASSWORD"]
  host = credentials["HOST"]
  port = int(credentials["PORT"])
  username = credentials["USERNAME"]

  psql_db = PostgresqlDatabase(
      database,
      user=username, 
      password=password,
      host=host,
      port=port
    )

class BaseModel(Model):
  class Meta:
    database = psql_db


class Theme(BaseModel):
  
  id=UUIDField(primary_key=True, default=uuid.uuid4)
  theme_name = CharField(null=True)
  

class Ksb(BaseModel):

  id = UUIDField(primary_key=True, default=uuid.uuid4)
  ksb_type = CharField(null=True)
  ksb_code = IntegerField(null=True)
  description = TextField()
  created_at = DateTimeField(default=datetime.datetime.now)
  updated_at = DateTimeField(default=datetime.datetime.now)


  def ksb_type_validator(self):
    if self.ksb_type not in KSB_TYPE_CHOICES:
      raise ValueError(f"{self.ksb_type} is not a valid ksb_type")
    else:
      self.ksb_type = self.ksb_type.capitalize()
      
  def ksb_code_validator(self):
    if isinstance(self.ksb_code, int):
      if self.ksb_code < 1 or self.ksb_code > 50:
        raise ValueError(f"{self.ksb_code} is not a valid ksb code, choose an int from 1 to 50")

    else:
      raise ValueError(f"{self.ksb_code} is of type: {type(self.ksb_code).__name__}, it needs to be an integer")
  
  def ksb_description_validator(self):
     if len(self.description) < 15 or len(self.description) > 300:
      raise ValueError(f"description needs to be more than 15 characters and less than 300 characters in length")
       
       
  def save(self, **kwargs):
    self.ksb_type_validator()
    self.ksb_code_validator()
    self.ksb_description_validator()
    
    super(Ksb, self).save(**kwargs)

class ThemeKsb(BaseModel):
    theme_id = ForeignKeyField(Theme, backref = 'ksbs', on_delete='CASCADE')
    ksb_id = ForeignKeyField(Ksb, backref = 'themes', on_delete='CASCADE')
    class Meta:
        primary_key = CompositeKey('theme_id', 'ksb_id')
