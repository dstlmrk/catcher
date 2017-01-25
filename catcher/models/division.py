from sqlalchemy import Column, Integer, String
from catcher.models.base import Base


class Division(Base):
    __tablename__ = 'division'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    @staticmethod
    def get_all(session):
        return [team for team in session.query(Division)]
