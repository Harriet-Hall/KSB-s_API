from flask import Flask
from peewee import *
import os 
from dotenv import load_dotenv
app = Flask(__name__)

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
 pass