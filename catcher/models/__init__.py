from models import *
from connection import *

from user import *
from team import *



from iso3166 import countries

import peewee as pw
import connection

# class MySQLModel(pw.Model):
#     """A base model that will use our MySQL database"""

#     def __str__(self):
#         return str(model_to_dict(self))

#     class Meta:
#         database = db

# class CountryCode(pw.FixedCharField):
    
#     def db_value(self, value):
#         """Check if field is country by ISO 3166-1 alpha-3"""
#         print "======================================"
#         print value
#         if value is None:
#             return value
#         try:
#             countries.get(value)
#         except KeyError as ex:
#             raise KeyError('Country by ISO 3166-1 alpha-3 not found')
#         else:
#             return value
