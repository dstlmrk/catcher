#

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm.exc import NoResultFound
from catcher.models.base import Base, session
# from catcher.models import Role, Email, ApiKey


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    division_id = Column(Integer, ForeignKey('division.id'))
    name = Column(String)
    shortcut = Column(String)
    city = Column(String)
    country = Column(String)
    cald_id = Column(Integer)
    user_id = Column(Integer)



    # email = Column(String)
    # password = Column(String)
    # created_at = Column(DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    # role_id = Column(Integer, ForeignKey('role.id'))
    #


# id, division_id, name, shortcut, city, country, cald_id, user_id