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
 id = UUIDField(primary_key=True)
 ksb_type = CharField()
 ksb_code = IntegerField()
 description = TextField()


