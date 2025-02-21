from peewee import *
import os 
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
    # table_name = "Ksbs"


class Ksb(BaseModel):
  KSB_TYPE_CHOICES = [
    'Knowledge', 'knowledge',
    'Skill', 'skill',
    'Behaviour', 'behaviour'
        ]
  id = UUIDField(primary_key=True)
  ksb_type = CharField()
  ksb_code = IntegerField()
  description = TextField()

  def ksb_type_validator(self):
    if self.ksb_type not in self.KSB_TYPE_CHOICES:
      raise ValueError(f"{self.ksb_type} is not a valid ksb_type")
    else:
      self.ksb_type = self.ksb_type.capitalize()
      
  def ksb_code_validator(self):
    if self.ksb_code < 1 or self.ksb_code > 25:
      raise ValueError(f"{self.ksb_code} is not a valid ksb_code, choose a number from 1 to 25")
       
  def save(self, **kwargs):
    self.ksb_type_validator()
    super(Ksb, self).save(**kwargs)
