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
  ksb_type = CharField(choices=KSB_TYPE_CHOICES)
  ksb_code = IntegerField()
  description = TextField()

  def save(self, **kwargs):
    if self.ksb_type not in self.KSB_TYPE_CHOICES:
      raise ValueError(f"{self.ksb_type} is not a valid ksb_type")
    else:
      self.ksb_type = self.ksb_type.capitalize()
      super(Ksb, self).save(**kwargs)
