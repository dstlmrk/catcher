from peewee import CharField
from catcher.models import MySQLModel

class Division(MySQLModel):
    division = CharField()
