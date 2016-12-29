#

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
# from sqlalchemy.orm.exc import NoResultFound
from catcher.models.base import Base, session
# from catcher.models import Role, Email, ApiKey


class Team(Base):
    __tablename__ = 'team'

    id = Column(Integer, primary_key=True)
    # email = Column(String)
    # password = Column(String)
    # created_at = Column(DateTime, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    # role_id = Column(Integer, ForeignKey('role.id'))
    #
    # def __repr__(self):
    #     return "<User(id='%s', email='%s', password='%s', created_at='%s', role_id='%s')>" % (
    #         self.id, self.email, self.password, self.created_at, self.role_id)



# id, division_id, name, shortcut, city, country, cald_id, user_id