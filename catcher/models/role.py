from sqlalchemy import Column, Integer, String
from catcher.models.base import Base, session


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    @staticmethod
    @session
    def get_all(_session):
        return [team for team in _session.query(Role)]
