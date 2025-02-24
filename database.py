from peewee import *
import os 
from utils import KSB_TYPE_CHOICES
from dotenv import load_dotenv

load_dotenv()


psql_db = PostgresqlDatabase(
    os.getenv("DATABASE"),
    user=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    host=os.getenv("HOST"),
    port=os.getenv("PORT")
)

class BaseModel(Model):
  class Meta:
    database = psql_db

class Ksb(BaseModel):

  id = UUIDField(primary_key=True)
  ksb_type = CharField(null=True)
  ksb_code = IntegerField(null=True)
  description = CharField(max_length=255, unique=True, null=True)

  def ksb_type_validator(self):
    if self.ksb_type not in KSB_TYPE_CHOICES:
      raise ValueError(f"{self.ksb_type} is not a valid ksb_type")
    else:
      self.ksb_type = self.ksb_type.capitalize()
      
  def ksb_code_validator(self):
    if self.ksb_code < 1 or self.ksb_code > 50 or type(self.ksb_code) is not int:
      raise ValueError(f"{self.ksb_code} is not a valid ksb_code, choose a int from 1 to 25")
  
  def ksb_description_validator(self):
     if len(self.description) < 15 or len(self.description) > 300:
      raise ValueError(f"description needs to be more than 15 characters and less than 300 characters in length")
       
       
  def save(self, **kwargs):
    self.ksb_type_validator()
    self.ksb_code_validator()
    
    super(Ksb, self).save(**kwargs)
