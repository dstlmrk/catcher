import connection
from peewee import Model, FixedCharField
from playhouse.shortcuts import model_to_dict
from iso3166 import countries

db = connection.connect_database()


class MySQLModel(Model):
    """A base model that will use our MySQL database"""

    def __str__(self):
        return str(model_to_dict(self))

    class Meta:
        database = db


class CountryCode(FixedCharField):
    def db_value(self, value):
        '''Check if field is country by ISO 3166-1 alpha-3'''
        if value is None:
            return value
        try:
            countries.get(value)
        except KeyError as ex:
            raise KeyError('Country by ISO 3166-1 alpha-3 not found')
        else:
            return value
